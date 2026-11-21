# Rekordbox Migrator — Project Outline

## 1. Overview

A locally hosted web application that automatically migrates tracks from Apple Music to Spotify in rekordbox 7 while preserving existing DJ preparation metadata.

### 1.1. Goal

- Automatically replace Apple Music tracks with their Spotify equivalents in rekordbox.
- Preserve:
  - Hot Cues (positions, slots, colors, labels)
  - Memory Cues (positions, labels)
  - Beatgrids (BPM, beat positions, tempo changes)
  - Saved Loops (start/end positions, settings)
- Support migration of the entire rekordbox library.
- Require minimal user intervention.
- Preserve original tracks and provide rollback capabilities.

### 1.2. Key Constraints

- Rekordbox has no documented public API for transferring metadata between streaming services.
- Apple Music and Spotify tracks may have different audio offsets, durations, or versions.
- Rekordbox stores preparation data in its internal database and analysis files.
- Direct database modifications may be unsupported and could cause corruption.
- Spotify tracks must be registered as native Spotify entries in rekordbox.
- Feasibility of writing preparation metadata to Spotify entries must be verified before full development.

## 2. User Experience

### 2.1. Initial Setup

1. Launch the local application at `http://localhost:3000`.
2. Automatically detect the rekordbox installation and library.
3. Detect the installed rekordbox version.
4. Connect Spotify through OAuth.
5. Verify that the library is accessible.
6. Create an initial backup.

### 2.2. Main Dashboard

Display:

- Number of Apple Music tracks detected.
- Number of tracks matched to Spotify.
- Number of tracks without reliable matches.
- Number of tracks successfully migrated.
- Number of tracks skipped or failed.
- Overall migration progress.
- Current migration stage.

Main actions:

- **Scan Library**
- **Match Tracks**
- **Start Migration**
- **Pause / Resume**
- **View Results**
- **Restore Backup**

### 2.3. Migration Workflow

1. Scan all Apple Music tracks in rekordbox.
2. Extract track metadata and DJ preparation data.
3. Automatically find equivalent tracks on Spotify.
4. Validate matches and identify timing differences where possible.
5. Prepare Spotify entries inside rekordbox.
6. Transfer supported metadata to destination tracks.
7. Validate transferred data.
8. Generate a migration report.
9. Keep original Apple Music tracks unchanged.

The app should require no manual matching for a normal migration. Uncertain matches should be skipped automatically.

## 3. Core Features

### 3.1. Rekordbox Library Scanner

**Purpose:** Read and understand the existing rekordbox library.

Features:

- Automatically locate the rekordbox database and analysis files.
- Use `pyrekordbox` and compatible database readers.
- Identify Apple Music tracks.
- Extract:
  - Rekordbox track ID
  - Apple Music track identifier
  - Title
  - Artist
  - Album
  - Duration
  - ISRC, when available
  - BPM and key
  - Hot Cues
  - Memory Cues
  - Saved Loops
  - Beatgrid information
- Detect Spotify tracks already present in the collection.
- Save a local snapshot of all extracted metadata.
- Perform scanning using read-only access.

### 3.2. Spotify Track Matching

**Purpose:** Automatically identify equivalent Spotify tracks.

Matching methods, in priority order:

1. ISRC matching with additional metadata verification.
2. Exact title, artist, version, and duration.
3. Normalized title and artist with close duration.
4. Fuzzy matching with stricter validation.

Special cases:

- Original vs. remastered versions
- Radio edits vs. extended mixes
- Explicit vs. clean versions
- Live vs. studio recordings
- Remixes
- Duplicate releases
- Different audio intros or outros

Matching confidence:

- **High:** Automatically approve.
- **Medium:** Perform additional validation; skip if unresolved.
- **Low:** Skip.
- **Unmatched:** Record in the exception report.

Never migrate to a track without sufficient confidence.

### 3.3. Spotify Track Preparation

**Purpose:** Ensure Spotify tracks exist as legitimate rekordbox entries.

Workflow:

1. Collect matched Spotify track IDs.
2. Identify Spotify targets already in rekordbox.
3. Create temporary Spotify playlists for missing tracks when permitted by Spotify API access.
4. Use Windows UI automation to navigate rekordbox's Spotify integration.
5. Import or load Spotify tracks through supported rekordbox interface actions.
6. Allow rekordbox to create and analyze native Spotify entries.
7. Rescan the collection.
8. Associate every source Apple Music track with its destination rekordbox track ID.

Important considerations:

- Do not fabricate Spotify entries by changing Apple Music track URLs.
- Avoid creating duplicate destination tracks.
- Handle unavailable tracks and account restrictions.
- Support retries when track preparation fails.
- Treat UI automation as an experimental component requiring compatibility testing.

### 3.4. Metadata Transfer Engine

**Purpose:** Transfer DJ preparation data to the matched Spotify track.

#### Hot Cues

- Transfer cue positions.
- Preserve cue slots.
- Preserve cue colors.
- Preserve cue names.
- Maintain cue ordering.

#### Memory Cues

- Transfer cue timestamps.
- Preserve cue names and supported properties.
- Preserve cue ordering.

#### Saved Loops

- Transfer start and end positions.
- Preserve supported loop settings.
- Preserve loop-related cue associations.

#### Beatgrids

- Preserve BPM.
- Transfer grid markers.
- Preserve tempo changes.
- Apply timing offsets when reliably determined.

#### Transfer Requirements

- Check target metadata before writing.
- Avoid overwriting unrelated existing metadata.
- Write only to verified target entries.
- Preserve the original Apple Music metadata.
- Validate each transfer after writing.
- Record every modification for rollback.

### 3.5. Timing Alignment Engine

**Purpose:** Prevent transferred cues and beatgrids from becoming misaligned.

Features:

- Compare source and destination durations.
- Compare BPM and available beatgrid information.
- Detect potential audio offsets.
- Distinguish recording-version differences from simple timing offsets.
- Adjust cue, loop, and beatgrid timestamps when an offset is reliably established.
- Skip unsafe transfers.

Example:

- Apple Music Hot Cue: `01:12.500`
- Spotify audio offset: `+120 ms`
- Adjusted Spotify Hot Cue: `01:12.620`

Limitations:

- Track metadata alone cannot guarantee accurate musical alignment.
- Full Spotify audio is not generally available through its Web API for waveform comparison.
- If alignment cannot be established, mark the transfer as requiring audio verification or skip it, depending on the configured safety policy.

### 3.6. Batch Migration Engine

**Purpose:** Process the entire library automatically.

Features:

- Queue all matched tracks.
- Process tracks in manageable batches.
- Track each migration stage.
- Skip unresolved matches.
- Retry temporary failures.
- Save progress after each batch.
- Resume interrupted migrations.
- Avoid duplicate processing.
- Support pause and cancellation.
- Maintain detailed logs.

Track states:

1. `discovered`
2. `matched`
3. `target_prepared`
4. `transfer_staged`
5. `transferred`
6. `verified`

Exception states:

- `unmatched`
- `skipped`
- `failed`
- `requires_verification`

## 4. Technical Architecture

### 4.1. Frontend

**Recommended:** React + Vite

Pages:

- Dashboard
- Connections / Setup
- Library Scanner
- Track Matching Results
- Migration Progress
- Migration Report
- Settings / Backup Management

Features:

- Real-time progress updates.
- Track-level migration status.
- Searchable and filterable results.
- Error explanations.
- Backup restoration controls.

### 4.2. Backend

**Recommended:** Python + FastAPI

Responsibilities:

- Rekordbox database access.
- Spotify API integration.
- Track matching.
- Metadata extraction and transfer.
- Timing calculations.
- Windows UI automation coordination.
- Background job processing.
- Backup creation and restoration.
- Validation and reporting.

### 4.3. Integrations

#### Rekordbox

- `pyrekordbox`
- SQLCipher-compatible database access
- Analysis-file parsing
- Windows UI Automation / `pywinauto`

#### Spotify

- Spotify Web API
- OAuth PKCE
- Track search
- Track metadata retrieval
- Temporary playlist management, subject to API permissions

#### Local Storage

- SQLite for migration state.
- JSON snapshots for track metadata.
- Versioned backups.
- Structured logs.

### 4.4. Project Structure

```text
rekordbox-migrator/
├── frontend/
│   ├── components/
│   ├── pages/
│   └── services/
├── backend/
│   ├── api/
│   ├── rekordbox/
│   │   ├── scanner.py
│   │   ├── metadata.py
│   │   └── writer.py
│   ├── spotify/
│   │   ├── auth.py
│   │   ├── search.py
│   │   └── playlists.py
│   ├── matching/
│   │   └── matcher.py
│   ├── migration/
│   │   ├── orchestrator.py
│   │   ├── transfer.py
│   │   ├── alignment.py
│   │   └── validator.py
│   ├── automation/
│   │   └── rekordbox_ui.py
│   ├── backup/
│   └── storage/
├── tests/
└── README.md
```

## 5. Data Model

### 5.1. SourceTrack

- Rekordbox ID
- Apple Music ID
- Track metadata
- Cue metadata
- Loop metadata
- Beatgrid metadata

### 5.2. TargetTrack

- Spotify ID
- Destination rekordbox ID
- Track metadata
- Analysis status

### 5.3. TrackMatch

- Source track ID
- Destination track ID
- Match confidence
- Match reasoning
- Match status

### 5.4. MigrationJob

- Job ID
- Source track
- Destination track
- Current stage
- Migration status
- Retry count
- Error details

### 5.5. Backup

- Backup ID
- Timestamp
- Original library location
- Snapshot location
- Integrity checksums

### 5.6. ValidationResult

- Transferred Hot Cue count
- Transferred Memory Cue count
- Transferred loop count
- Beatgrid comparison
- Timestamp differences
- Validation status

## 6. Safety and Reliability

### 6.1. Backup System

- Automatically back up the rekordbox library before migration.
- Include database, analysis files, and relevant journal files.
- Verify backup integrity.
- Maintain original track records.
- Support full rollback.

### 6.2. Safe Database Modifications

- Never modify the live database while rekordbox is running.
- Use isolated staging copies where possible.
- Validate database integrity before and after writes.
- Only modify positively identified destination records.
- Reject unsupported rekordbox versions.
- Maintain an audit log of all modifications.

### 6.3. Failure Recovery

- Record migration progress continuously.
- Resume incomplete jobs.
- Retry recoverable errors.
- Skip tracks that cannot be safely migrated.
- Preserve backups after failure.
- Provide clear error explanations.

### 6.4. Security

- Host the backend on `127.0.0.1`.
- Store credentials locally.
- Use Spotify OAuth PKCE.
- Avoid exposing database access remotely.
- Never upload rekordbox library data to an external server unless explicitly required and authorized.

## 7. Validation and Reporting

### 7.1. Validation

After migration:

- Verify Spotify target entries exist.
- Verify cue counts.
- Compare cue positions and properties.
- Compare loop start/end positions.
- Compare beatgrid metadata.
- Confirm database integrity.
- Test that Spotify tracks load correctly in rekordbox.
- Distinguish structural validation from actual audio alignment validation.

### 7.2. Migration Report

Display:

- Total source tracks
- Successfully matched tracks
- Successfully transferred tracks
- Fully verified tracks
- Tracks requiring audio checks
- Skipped tracks
- Failed tracks

Each track should include:

- Original Apple Music track
- Matched Spotify track
- Match confidence
- Metadata transferred
- Timing adjustments
- Migration status
- Error or warning details

### 7.3. Export

- CSV report
- JSON report
- Detailed error log

## 8. Development Roadmap

### Phase 1 — Feasibility Proof

**Objective:** Confirm that metadata can be migrated between Apple Music and Spotify rekordbox entries.

Tasks:

1. Inspect the rekordbox database and analysis files.
2. Extract metadata from one Apple Music track.
3. Identify its corresponding Spotify track.
4. Register the Spotify track in rekordbox.
5. Test transferring one Hot Cue.
6. Reopen rekordbox and verify the result.
7. Test cue alignment through playback.
8. Restore the original library to confirm rollback works.

**Success criteria:** A transferred cue survives restarting rekordbox, appears on the correct Spotify track, and aligns with the intended musical moment.

**Do not proceed to full automation until this is proven.**

### Phase 2 — Complete Metadata Transfer

**Objective:** Support every required metadata type.

Tasks:

- Hot Cue transfer
- Memory Cue transfer
- Saved Loop transfer
- Beatgrid transfer
- Timing adjustment
- Metadata validation
- Backup and rollback testing

**Success criteria:** All four metadata categories survive transfer in representative test cases.

### Phase 3 — Spotify Matching and Automation

**Objective:** Eliminate manual track preparation.

Tasks:

- Spotify authentication
- Automatic track matching
- Confidence scoring
- Temporary playlist creation
- Native Spotify track preparation
- Windows UI automation
- Batch migration
- Retry/resume functionality

**Success criteria:** A representative batch migrates without manual track-by-track intervention.

### Phase 4 — Web Interface

**Objective:** Deliver a complete local user experience.

Tasks:

- Setup page
- Dashboard
- Match statistics
- Progress monitoring
- Migration controls
- Error reporting
- Backup restoration
- Results export

### Phase 5 — Reliability and Packaging

**Objective:** Make the application safe for full-library migrations.

Tasks:

- Rekordbox version compatibility checks
- Large-library testing
- Interrupted-migration recovery
- Database integrity testing
- Duplicate-track handling
- Timing mismatch detection
- Windows installer and launcher
- User documentation

## 9. MVP Requirements

### Must Have

- Automatic Apple Music track discovery.
- Automatic Spotify track matching.
- Native Spotify track preparation.
- Hot Cue transfer.
- Memory Cue transfer.
- Beatgrid transfer.
- Saved Loop transfer.
- Automatic batch processing.
- Backup and rollback.
- Track-level validation.
- Migration progress and error reporting.

### Nice to Have

- Playlist structure migration.
- Ratings, tags, and comments transfer.
- Historical migration comparisons.
- Advanced track matching controls.
- Manual override for skipped tracks.
- Compatibility with other streaming services.

### Out of Scope

- Downloading or extracting protected streaming audio.
- Circumventing streaming DRM.
- Replacing Spotify's authentication system.
- Guaranteed transfer to different song versions.
- Deleting original Apple Music entries automatically.
- Cloud-hosted library migration.

## 10. Main Technical Risks

| Risk | Approach |
|---|---|
| Rekordbox database changes between versions | Version detection and compatibility tests |
| Encrypted database access | Use established compatible readers |
| Spotify target preparation | Test native rekordbox workflow and UI automation |
| Cue transfer to streaming entries unsupported | Prove feasibility before full development |
| Different audio timing | Alignment checks and conservative skipping |
| Incorrect song matching | Strict confidence thresholds |
| Database corruption | Verified backups, closed-app writes, rollback |
| Failed batch processing | Persistent state and retry/resume |

## 11. Final Success Criteria

The application is successful when it can:

1. Detect the entire Apple Music collection automatically.
2. Find the correct Spotify counterparts for reliably matchable tracks.
3. Register those tracks natively inside rekordbox.
4. Preserve Hot Cues, Memory Cues, beatgrids, and saved loops.
5. Maintain correct musical timing for verified transfers.
6. Process large libraries without manual track-by-track actions.
7. Skip uncertain tracks rather than corrupting metadata.
8. Preserve the original Apple Music library.
9. Recover safely from interruptions and failures.
10. Produce a clear report of migrated, skipped, and failed tracks.

**Primary engineering priority:** Prove reliable metadata transfer from one Apple Music rekordbox entry to one Spotify rekordbox entry before implementing full-library automation.

## 12. References

- [pyrekordbox](https://github.com/dylanljones/pyrekordbox) — Rekordbox database and analysis-file access
- [djlib-doctor](https://pypi.org/project/djlib-doctor/) — Reference for rekordbox metadata handling
- [Spotify Web API](https://developer.spotify.com/documentation/web-api) — Search, metadata, authentication, and playlists
- [Rekordbox Streaming FAQ](https://rekordbox.com/en/support/faq/streaming-7/) — Streaming integration and limitations
- [pywinauto](https://pywinauto.readthedocs.io/) — Windows desktop UI automation
