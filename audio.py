"""
Audio streaming using OpenAI's Realtime API.
This module captures audio from the microphone, sends it to OpenAI's Realtime API, and plays back the assistant's audio response in real-time.
"""

import asyncio
import base64
import json
import numpy as np
import pyaudio
import websockets
from rich.console import Console

from config import Config

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
HARDWARE_RATE = 44100
OPENAI_RATE = 24000
CHUNK = 2400


async def audio_stream(config: Config, console: Console):
    """Streams audio to and from OpenAI's Realtime API using WebSockets."""

    url = f"wss://api.openai.com/v1/realtime?model={config.sts_model}"
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "OpenAI-Beta": "realtime=v1",
    }

    async with websockets.connect(url, additional_headers=headers) as ws:
        console.print("[bold green]Connected to Realtime API![/]\n")

        # Initialize Session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": "You are a pragmatic, matter-of-fact assistant. Brief and clinical.",
                "voice": config.tts_voice,
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.3,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 400
                }
            }
        }))

        p = pyaudio.PyAudio()
        loop = asyncio.get_running_loop()
        audio_queue = asyncio.Queue()

        def mic_callback(input_data, frame_count, time_info, status_flags):
            audio_array = np.frombuffer(input_data, dtype=np.int16).astype(np.float32)

            # Simple linear downsampling (44100 → 24000)
            old_len = len(audio_array)
            new_len = int(old_len * (OPENAI_RATE / HARDWARE_RATE))
            indices = np.linspace(0, old_len - 1, new_len)
            resampled = np.interp(indices, np.arange(old_len), audio_array)

            resampled = np.clip(resampled, -32768, 32767).astype(np.int16).tobytes()
            asyncio.run_coroutine_threadsafe(audio_queue.put(resampled), loop)
            return (None, pyaudio.paContinue)

        # Open Input Stream (Mic) with callback
        mic_stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=HARDWARE_RATE,
            input=True,
            input_device_index=0,
            frames_per_buffer=CHUNK,
            stream_callback=mic_callback
        )

        # Open Output Stream (Speaker)
        spk_stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=OPENAI_RATE,
            output=True,
            frames_per_buffer=CHUNK
        )

        async def send_mic_audio():
            try:
                while True:
                    downsampled_audio = await audio_queue.get()
                    encoded_audio = base64.b64encode(downsampled_audio).decode('utf-8')
                    await ws.send(json.dumps({
                        "type": "input_audio_buffer.append",
                        "audio": encoded_audio
                    }))
            except OSError as e:
                console.print(f"[red]Mic Error: {e}[/]")

        async def receive_events():
            async for message in ws:
                event = json.loads(message)

                if event["type"] == "response.audio.delta":
                    audio_content = base64.b64decode(event["delta"])
                    spk_stream.write(audio_content)

                elif event["type"] in ["input_audio_buffer.speech_started", "input_audio_buffer.speech_stopped", "response.audio_transcript.done"]:
                    console.print(f"[yellow]Event: {event['type']}[/]")

                elif event["type"] == "response.audio_transcript.delta":
                    console.print(event["delta"], end="", style="bright_red")

                elif event["type"] == "error":
                    console.print(f"\n[bold red]API Error:[/] {event['error']}")

        # Run both tasks concurrently
        try:
            await asyncio.gather(send_mic_audio(), receive_events())
        except asyncio.CancelledError:
            pass
        finally:
            mic_stream.stop_stream()
            mic_stream.close()
            spk_stream.stop_stream()
            spk_stream.close()
            p.terminate()
