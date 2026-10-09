# Livestreams and chat replay

Read this when the source is still live, or when a livestream VOD's chat replay is in scope. Downloads, transcription, and frames follow [MEDIA.md](MEDIA.md) as for any recording.

## Livestream in progress

```sh
yt-dlp --ignore-config --no-playlist --print "%(live_status)s %(duration)s" "$video_url"
yt-dlp --ignore-config --no-playlist -N 2 -f "$audio_format_id" \
  -o "$archive_dir/%(id)s.audio.%(ext)s" "$video_url"
```

- `live_status` runs `is_live` while the stream is on, `post_live` once it ends, and `was_live` some time later. Poll it every five to ten minutes with a scheduled job the harness owns; a background shell loop is killed at its time limit. Tell the job what to do at each status, and ask before installing anything on the machine for it.
- Download at `post_live`. In two runs the full recording was already there, as DASH-only formats with no captions; `was_live` came 35 to 45 minutes later and brought only the chat replay track. Check the downloaded duration against the reported one.
- Two downloads at once with `-N 8` each died within seconds: `HTTP Error 401: Unauthorized` on fragment after fragment until the retries ran out. One download at a time with `-N 2` finished clean twice; which of the two changes mattered is unknown. A failed run leaves `.part` files, and the next run resumes from them.
- The listed size of the DASH video format at `post_live` ran to four to six times the real file. Check free disk before downloading, and quote the size of the downloaded file instead.
- Captions may never appear: none existed at `post_live` or at `was_live` in two runs. Plan on fresh transcription and re-check captions once.
- A VOD can be unlisted or removed after the stream. Download promptly, and note in the ledger whether the archive is backed up.
- Worked on two YouTube livestreams in October 2026.

## Chat replay

```sh
yt-dlp --ignore-config --no-playlist --skip-download --write-subs \
  --sub-langs live_chat -o "$archive_dir/%(id)s.%(ext)s" "$video_url"
python3 -I "$skill_dir/scripts/flatten_chat.py" "$archive_dir/$video_id.live_chat.json" "$notes_dir/chat.md"
```

- YouTube lists the replay as a subtitle track named `live_chat` in `--list-subs`. A VOD without it has replay turned off or not processed yet: log a gap and re-check later if it matters. For a stream that just ended, the track arrived with `was_live`, after the media itself was already downloadable.
- `scripts/flatten_chat.py` writes one line per message sorted by source time, tags the channel owner, moderators, and paid messages, and prints the message counts for the ledger. The raw file is JSON lines: `replayChatItemAction.videoOffsetTimeMsec` is source time, and the text sits under `actions[].addChatItemAction.item` as `message.runs`, in case the script falls behind a format change. Keep the raw file.
- Messages sent before the recording starts are all stamped zero, so they carry no usable time.
- Paid messages are the ones a speaker most often reads aloud, and the reply can come half an hour to nearly an hour after the message. Pair a question with its answer by searching the transcript for the message's words; matching times alone will miss it.
- Moderators' messages often say which platform's chat the speaker reads. A stream simulcast to Twitch has a second chat there. yt-dlp refused one subscriber-only Twitch VOD without a logged-in account (October 2026); whether its chat can be reached another way is untested, so log it as a gap unless the user arranges access.
- Worked on two YouTube VODs in October 2026.
