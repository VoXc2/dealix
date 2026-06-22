# Contributing to Dealix

Thank you for your interest in contributing to Dealix! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct (see CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue tracker as a bug might already be documented.

**When creating a bug report, include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, Node version, Docker version)
- Screenshots if applicable
- Relevant log output

### Suggesting Features

Feature suggestions are welcome. When suggesting a feature:
- Explain the problem it solves
- Describe the expected behavior
- Provide examples if possible
- Consider edge cases

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

**PR Requirements:**
- Clear description of changes
- Tests for new functionality
- Updated documentation
- Passes all CI checks
- Follows code style guidelines

## Development Setup

### Prerequisites
- Node.js 20+
- Python 3.11+
- Docker 24+ (optional)
- MySQL 8.0+ (or use Docker)

### Quick Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/dealix.git
cd dealix

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Setup database
npm run db:push

# Start development server
npm run dev
```

### Project Structure

```
dealix/
├── api/              # Backend API (Hono + tRPC)
├── src/              # Frontend (React + Vite)
├── db/               # Database schema (Drizzle)
├── scripts/          # Operational scripts
├── clients/          # Client delivery templates
├── business/         # Business documentation
├── docs/             # Technical documentation
├── company_os/       # Internal operations
└── dist/             # Build output
```

## Code Style

### TypeScript
- Use strict mode
- Prefer explicit types over `any`
- Use meaningful variable names
- Add JSDoc comments for public APIs

### React
- Use functional components
- Prefer hooks over class components
- Keep components small and focused
- Use TypeScript for props

### API
- All routes through tRPC
- Type-safe inputs and outputs
- Proper error handling
- Input validation

## Testing

```bash
# Run all checks
npm run check

# Run production checks
npm run production-check

# Safety verification
npm run outbound-dry

# Build verification
npm run build
```

## Commit Guidelines

Use conventional commits:

```
feat: new feature
fix: bug fix
docs: documentation changes
style: formatting, missing semi colons, etc
refactor: code change that neither fixes a bug nor adds a feature
test: adding missing tests
chore: maintenance
```

## Security

- Never commit `.env` files
- Never commit secrets or credentials
- Report security vulnerabilities privately to maintainers
- Follow security best practices

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for deployment changes
- Add JSDoc comments for new APIs
- Update docs/ for new features

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing!
