# Setup — ShreyanshJain105 animated GitHub profile

1. The profile repository must be public and named exactly `ShreyanshJain105`: https://github.com/ShreyanshJain105
2. Copy this package into that repository root and merge with existing files; do not delete unrelated files.
3. Add a repository secret named `GH_TOKEN` using a fine-grained/classic token that can read your public user profile (`read:user`). The renderer uses GitHub GraphQL `contributionsCollection` for the exact daily contribution calendar.
4. Enable GitHub Actions and run **Update animated profile cards** once manually. It then refreshes daily at 02:17 UTC and commits changed SVG/data files automatically.
5. Local rendering requires Python 3.10+: `python scripts/render_profile.py`.

The profile avatar is loaded from `https://github.com/ShreyanshJain105.png`. The `rea`, `coolify`, and `ruflo` entries are labelled as forks, not original projects. The contribution screenshot is a dated snapshot from 19 November 2026; the generated SVG cards update automatically after Actions runs.
