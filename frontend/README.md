# RainCast AI - Frontend Presentation Layer

This directory houses the client-side presentation assets, templates, and internationalization files for RainCast AI.

## Architecture

- **`templates/`**: Server-rendered Jinja2 HTML5 templates styled with Tailwind CSS:
  - `base.html`: Common dark-navy shell, sticky header with language switcher, navigation links, and IMD statutory disclaimer footer.
  - `index.html`: Platform overview, live KPI badges, workflow pipeline, and module cards.
  - `dashboard.html`: Descriptive climate analytics, dynamic location filters, 125-year timeline (1901–2025), and monthly profiles.
  - `predict.html`: Multi-horizon ML prediction, IMD anomaly speedometer gauge, expanding confidence cone, and agricultural suitability advisories.
  - `assistant.html`: Trilingual conversational climate reasoning chat interface with quick-prompt chips.
  - `models.html`: Model performance comparison matrix, parity scatter plot, and residual error distribution.
  - `reports.html`: Publication-grade PDF download, cleaned CSV export, and SQLite audit activity table.
- **`static/`**:
  - `translations.js`: Comprehensive Trilingual translation dictionary (English, Hindi, Punjabi) and `I18nManager` client.
  - `logo.svg`: High-resolution vector branding mark.

## Internationalization (i18n)

The frontend features dynamic language switching (English, Hindi, Punjabi) using custom `data-i18n` attributes. Preferences are saved in browser `localStorage` under `raincast_lang` and synchronized across all charts and AI requests.

