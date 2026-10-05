# Media acquisition and timing

Examples of a local workflow with `yt-dlp`, `ffmpeg`, and whisper.cpp; any equivalent backend works. For flags beyond these, read the installed tool's `--help` or its docs: [yt-dlp](https://github.com/yt-dlp/yt-dlp#usage-and-options), [FFmpeg](https://ffmpeg.org/ffmpeg.html), [whisper.cpp](https://github.com/ggml-org/whisper.cpp#quick-start).

## Captions

```sh
yt-dlp --ignore-config --no-playlist --list-subs "$video_url"
yt-dlp --ignore-config --no-playlist --skip-download --write-auto-subs \
  --sub-langs 'en-orig' --sub-format json3 \
  -o "$archive_dir/%(id)s.%(ext)s" "$video_url"
```

- `--ignore-config --no-playlist` keeps the user's config and the surrounding playlist out of the run. Quote the URL.
- List tracks first and pick the real source-language one. On YouTube the untranslated automatic track is usually `<lang>-orig` (`en-orig` above); other listed languages are machine translations. Use `--write-subs` for authored subtitles.
- Prefer `json3` for YouTube automatic captions: each event carries only its new words, with timing. Flatten it by joining each event's `segs` and skipping `aAppend` events, which hold only line breaks. The VTT form of the same track repeats every line across rolling cues.

## Audio and video downloads

```sh
yt-dlp --ignore-config --no-playlist --list-formats "$video_url"
yt-dlp --ignore-config --no-playlist -f "$format_id" \
  -o "$archive_dir/%(id)s.%(ext)s" "$video_url"
```

- Pick a video format whose resolution makes small on-screen text readable. For audio, select an audio format; the `bestaudio/best` fallback may bring video along.
- `HTTP Error 403: Forbidden` on the media download usually means the default player client is blocked. Switch clients with `--extractor-args "youtube:player_client=web_embedded"` (worked in September 2026), on the format listing too, since format ids differ per client.
- Run `yt-dlp` unpiped, or check its own exit status: piped into `tail`, a failed download reports the pipe's success.
- `--download-sections '*HH:MM:SS-HH:MM:SS'` fetches a window cut at keyframes, so the clip's true start can differ from the request. Verify the offset (next section) before trusting it.
- When an extractor fails some other way, check `yt-dlp --version` and the error text, and retry only after changing something the error points at.

## Audio and transcription

```sh
ffmpeg -n -ss "$start_seconds" -t "$duration_seconds" -i "$audio_path" \
  -vn -ar 16000 -ac 1 -c:a pcm_s16le "$archive_dir/excerpt-$start_seconds.wav"
```

- whisper.cpp reads 16 kHz mono PCM WAV, which this produces. `-n` refuses to overwrite, so give each excerpt its own filename.
- `$start_seconds` is the clip's **offset**: source time = offset + clip time. Store the offset with the clip. Exit status says nothing about timing, so check the duration with `ffprobe` and spot-check a known line against the source.
- Match the model to the language: `.en` models handle English only.
- Silence, music, and poor audio produce confident invented text. Check consequential passages against captions or the video.

## Frames

```sh
ffmpeg -n -ss "$clip_seconds" -i "$video_clip" -frames:v 1 "$frame_path"
ffmpeg -n -i "$video_clip" -vf "fps=1/10,scale=480:-1,tile=6x5" "$archive_dir/sheet-%03d.png"
```

- `-ss` before `-i` seeks straight to the frame; after `-i` it decodes the whole file up to that point.
- `$clip_seconds` is clip time, which equals source time only for a whole-file download. Otherwise derive source time from the clip's verified offset before naming or citing the image; nearby speech and recognizable visual transitions confirm alignment. Label a timestamp approximate when alignment is uncertain.
- Sample several frames around the moment and pick one after scrolling or transitions settle.
- Read frames with vision; confirm OCR output by eye for commands, filenames, and numbers.
- Keep enough context in the frame to identify the application or document, and keep the original beside any crop.
- The second command builds contact sheets for navigation: one tile per 10 seconds, 30 per sheet, read left to right. Homebrew's ffmpeg often lacks `drawtext`, so find a tile's time by counting. Tiles are candidates.
