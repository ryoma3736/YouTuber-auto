# YouTuber-auto 🎬

YouTube経済ニュース動画自動生成システム

Autonomous development powered by **Miyabi** - AI-driven development framework.

## YouTube Auto Generator

1日あたり複数本の経済ニュース動画を完全自動生成します。LINE経由でトリガーし、15-30分で動画が完成。

### 機能 ✅ All Complete!

- ✅ **AI経済ニュース検索**: Claude APIで最新ニュースを要約
- ✅ **対談台本自動生成**: 2人の対談形式で自然な会話を生成
- ✅ **音声生成**: Gemini TTS & ElevenLabs TTS
- ✅ **動画生成**: MoviePy + FFmpeg (字幕・BGM対応)
- ✅ **サムネイル生成**: PIL画像処理
- ✅ **YouTube自動アップロード**: YouTube Data API v3
- ✅ **LINE連携**: トリガー受信 & 実行結果通知
- ✅ **完全自動化**: 7ステップパイプライン統合

### Python Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run pipeline
python app/pipeline/run_pipeline.py

# Start web server
python main.py
```

## TypeScript Development (Miyabi Framework)

## Getting Started

### Prerequisites

```bash
# Set environment variables
cp .env.example .env
# Edit .env and add your tokens
```

### Installation

```bash
npm install
```

### Development

```bash
npm run dev          # Run development server
npm run build        # Build project
npm test             # Run tests
npm run typecheck    # Check types
npm run lint         # Lint code
```

## Project Structure

```
YouTuber-auto/
├── app/                    # Python application
│   ├── core/              # Core modules
│   │   ├── ai_news.py     # News search (Claude)
│   │   ├── ai_script.py   # Script generation (Claude)
│   │   ├── ai_metadata.py # Metadata generation (Claude)
│   │   ├── tts.py         # Text-to-speech (Gemini/ElevenLabs)
│   │   ├── video.py       # Video generation (MoviePy)
│   │   ├── thumbnail.py   # Thumbnail generation (PIL)
│   │   ├── youtube_uploader.py # YouTube API
│   │   ├── line_notify.py # LINE notifications
│   │   └── prompts.py     # Prompt management
│   ├── web/               # Web server
│   │   └── line_webhook.py # LINE webhook handler
│   └── pipeline/          # Pipeline orchestration
│       └── run_pipeline.py # Main pipeline
├── src/                   # TypeScript (Miyabi framework)
│   └── index.ts
├── .github/workflows/     # CI/CD automation
├── config.py              # Configuration
├── prompts.yaml           # AI prompts
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
├── DEPLOYMENT.md          # Deployment guide
└── main.py               # FastAPI entry point
```

## Miyabi Framework

This project uses **7 autonomous AI agents**:

1. **CoordinatorAgent** - Task planning & orchestration
2. **IssueAgent** - Automatic issue analysis & labeling
3. **CodeGenAgent** - AI-powered code generation
4. **ReviewAgent** - Code quality validation (80+ score)
5. **PRAgent** - Automatic PR creation
6. **DeploymentAgent** - CI/CD deployment automation
7. **TestAgent** - Test execution & coverage

### Workflow

1. **Create Issue**: Describe what you want to build
2. **Agents Work**: AI agents analyze, implement, test
3. **Review PR**: Check generated pull request
4. **Merge**: Automatic deployment

### Label System

Issues transition through states automatically:

- `📥 state:pending` - Waiting for agent assignment
- `🔍 state:analyzing` - Being analyzed
- `🏗️ state:implementing` - Code being written
- `👀 state:reviewing` - Under review
- `✅ state:done` - Completed & merged

## Commands

```bash
# Check project status
npx miyabi status

# Watch for changes (real-time)
npx miyabi status --watch

# Create new issue
gh issue create --title "Add feature" --body "Description"
```

## Configuration

### Environment Variables

Required variables (see `.env.example`):

- `GITHUB_TOKEN` - GitHub personal access token
- `ANTHROPIC_API_KEY` - Claude API key (optional for local development)
- `REPOSITORY` - Format: `owner/repo`

### GitHub Actions

Workflows are pre-configured in `.github/workflows/`:

- CI/CD pipeline
- Automated testing
- Deployment automation
- Agent execution triggers

**Note**: Set repository secrets at:
`https://github.com/ryoma3736/YouTuber-auto/settings/secrets/actions`

Required secrets:
- `GITHUB_TOKEN` (auto-provided by GitHub Actions)
- `ANTHROPIC_API_KEY` (add manually for agent execution)

## Documentation

- **Miyabi Framework**: https://github.com/ShunsukeHayashi/Miyabi
- **NPM Package**: https://www.npmjs.com/package/miyabi
- **Label System**: See `.github/labels.yml`
- **Agent Operations**: See `CLAUDE.md`
- **YouTube Economic News v1 Plan**: `docs/youtube-economic-news-plan.md`（Miyabi連動仕様とIssue分解ガイド）

## Support

- **Issues**: https://github.com/ShunsukeHayashi/Miyabi/issues
- **Discord**: [Coming soon]

## License

MIT

---

✨ Generated by [Miyabi](https://github.com/ShunsukeHayashi/Miyabi)
