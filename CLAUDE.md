# CLAUDE.md - AI Assistant Guide for IAG Repository

This document provides comprehensive guidance for AI assistants (like Claude) working on this codebase. It covers project structure, development workflows, conventions, and best practices.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Development Workflow](#development-workflow)
- [Coding Conventions](#coding-conventions)
- [AI Assistant Guidelines](#ai-assistant-guidelines)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

### About This Project

**Repository**: IAG
**Status**: In active development
**Primary Language**: [To be determined based on project setup]

### Tech Stack

- **Languages**: [To be documented]
- **Frameworks**: [To be documented]
- **Build Tools**: [To be documented]
- **Testing**: [To be documented]
- **CI/CD**: [To be documented]

### Key Dependencies

[To be documented as project develops]

---

## Repository Structure

```
IAG/
├── .git/                 # Git version control
├── CLAUDE.md            # This file - AI assistant guide
├── README.md            # Project documentation (to be created)
├── [src/]               # Source code (structure TBD)
├── [tests/]             # Test files (structure TBD)
├── [docs/]              # Additional documentation (structure TBD)
└── [config/]            # Configuration files (structure TBD)
```

### Important Directories

**To be documented as project structure is established**

---

## Development Workflow

### Git Branching Strategy

1. **Main Branch**: `main` or `master` (to be confirmed)
   - Production-ready code
   - Protected branch requiring pull requests

2. **Feature Branches**: `claude/feature-name-session-id`
   - All AI assistant work happens on feature branches
   - Branch naming convention: `claude/descriptive-name-<session-id>`
   - Always create from latest main branch

3. **Development Branch**: Check project instructions for designated branch

### Commit Guidelines

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(auth): add user authentication system

Implement JWT-based authentication with login and registration endpoints.
Includes middleware for protected routes.

Closes #123
```

```
fix(api): resolve null pointer exception in user service

Add null checks before accessing user properties to prevent crashes.
```

#### Commit Best Practices

- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Reference issue numbers when applicable
- Use imperative mood ("add feature" not "added feature")

### Pull Request Process

1. **Before Creating PR**:
   - Ensure all tests pass
   - Code follows project conventions
   - No merge conflicts with target branch
   - Commit history is clean and logical

2. **PR Description Should Include**:
   - Summary of changes
   - Testing performed
   - Related issue numbers
   - Breaking changes (if any)
   - Screenshots (for UI changes)

3. **PR Review**:
   - Address all review comments
   - Keep PR scope focused
   - Be responsive to feedback

---

## Coding Conventions

### General Principles

1. **Code Quality**
   - Write clean, readable, maintainable code
   - Follow DRY (Don't Repeat Yourself) principle
   - Keep functions small and focused
   - Use meaningful variable and function names

2. **Documentation**
   - Document complex logic with comments
   - Keep comments up-to-date
   - Write self-documenting code when possible
   - Maintain up-to-date README files

3. **Testing**
   - Write tests for new features
   - Maintain test coverage
   - Follow testing best practices
   - Include both unit and integration tests

### Language-Specific Conventions

**[To be documented based on project languages]**

### Code Style

**[To be documented - may include linter configs, formatters, etc.]**

---

## AI Assistant Guidelines

### Core Responsibilities

As an AI assistant working on this project, you should:

1. **Understand Before Changing**
   - Always read existing code before modifying
   - Understand the broader context
   - Follow existing patterns and conventions
   - Don't make assumptions about implementation

2. **Minimize Changes**
   - Make focused, targeted changes
   - Avoid over-engineering
   - Don't add unnecessary features
   - Keep solutions simple and direct

3. **Maintain Quality**
   - Follow coding conventions
   - Write tests for new code
   - Check for security vulnerabilities
   - Ensure backward compatibility (when needed)

4. **Communicate Clearly**
   - Explain changes and reasoning
   - Document complex decisions
   - Ask for clarification when uncertain
   - Provide context in commits and PRs

### Task Management

Use the TodoWrite tool to:
- Plan multi-step tasks
- Track progress on complex features
- Organize work systematically
- Ensure nothing is forgotten

**When to use TodoWrite**:
- Tasks with 3+ steps
- Complex implementations
- Multiple related changes
- User provides multiple tasks

**Task states**:
- `pending`: Not started
- `in_progress`: Currently working (ONE task at a time)
- `completed`: Finished successfully

### File Operations Best Practices

1. **Reading Files**
   - Use Read tool for file contents
   - Use Glob for finding files by pattern
   - Use Grep for searching file contents
   - Always read before editing

2. **Editing Files**
   - Use Edit tool for modifications
   - Preserve exact indentation
   - Make targeted changes
   - Verify changes don't break functionality

3. **Creating Files**
   - Only create when absolutely necessary
   - Prefer editing existing files
   - Follow project structure conventions
   - Don't create unnecessary documentation

### Security Considerations

Always check for:
- Command injection vulnerabilities
- XSS (Cross-Site Scripting)
- SQL injection
- Insecure dependencies
- Exposed secrets or credentials
- OWASP Top 10 vulnerabilities

**Never commit**:
- API keys or secrets
- Passwords or tokens
- `.env` files with credentials
- Private keys
- Sensitive configuration

### Git Operations

1. **Branching**
   ```bash
   # Create and checkout feature branch
   git checkout -b claude/feature-name-session-id
   ```

2. **Committing**
   ```bash
   # Stage changes
   git add <files>

   # Commit with descriptive message
   git commit -m "type(scope): description"
   ```

3. **Pushing**
   ```bash
   # Push to remote (with retry logic for network issues)
   git push -u origin claude/feature-name-session-id
   ```

4. **Creating PRs**
   ```bash
   # Use GitHub CLI
   gh pr create --title "Title" --body "Description"
   ```

### Code Review Readiness

Before marking work complete:
- [ ] All tests pass
- [ ] Code follows conventions
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated (if needed)
- [ ] Commits are clean and descriptive
- [ ] No unnecessary changes included

---

## Common Tasks

### Setting Up Development Environment

**[To be documented based on project requirements]**

```bash
# Example setup steps (update as needed)
# 1. Clone repository
# 2. Install dependencies
# 3. Configure environment
# 4. Run initial build/tests
```

### Running Tests

**[To be documented]**

```bash
# Example test commands
# npm test
# pytest
# cargo test
```

### Building the Project

**[To be documented]**

```bash
# Example build commands
# npm run build
# make build
# cargo build
```

### Debugging

**[To be documented based on project tooling]**

### Common Workflows

#### Adding a New Feature

1. Create feature branch
2. Implement feature with tests
3. Run all tests
4. Commit changes
5. Push to remote
6. Create pull request

#### Fixing a Bug

1. Reproduce the bug
2. Write failing test (if applicable)
3. Implement fix
4. Verify tests pass
5. Commit and push
6. Create pull request

#### Refactoring Code

1. Ensure tests exist for code being refactored
2. Make incremental changes
3. Run tests after each change
4. Keep commits atomic
5. Document significant changes

---

## Troubleshooting

### Common Issues

**[To be documented as common issues are identified]**

### Debug Strategies

1. **Build Failures**
   - Check error messages carefully
   - Verify dependencies are installed
   - Check for syntax errors
   - Review recent changes

2. **Test Failures**
   - Read test output thoroughly
   - Isolate failing tests
   - Check for environment issues
   - Verify test data/fixtures

3. **Git Issues**
   - Check branch status
   - Verify remote configuration
   - Review commit history
   - Check for merge conflicts

### Getting Help

- Review project documentation
- Check existing issues/PRs
- Examine similar code in codebase
- Ask for clarification when uncertain

---

## Updates and Maintenance

### Keeping This Document Current

This CLAUDE.md file should be updated when:
- Project structure changes significantly
- New conventions are established
- Common issues are identified
- Development workflow changes
- New tools or frameworks are added

### Document History

- **2026-01-22**: Initial creation - baseline AI assistant guide for empty repository

---

## Notes for AI Assistants

### Best Practices Summary

1. **Read First, Code Second**: Always understand existing code before making changes
2. **Stay Focused**: Only make changes directly related to the task
3. **Test Thoroughly**: Ensure changes don't break existing functionality
4. **Document Decisions**: Explain complex changes and reasoning
5. **Follow Conventions**: Match existing code style and patterns
6. **Communicate Clearly**: Keep commits, comments, and PRs clear and concise
7. **Ask When Uncertain**: Better to clarify than make assumptions
8. **Track Your Work**: Use TodoWrite for complex tasks

### What NOT to Do

- Don't create files unnecessarily
- Don't over-engineer solutions
- Don't add features beyond requirements
- Don't commit without testing
- Don't ignore existing conventions
- Don't make assumptions about user needs
- Don't add excessive documentation
- Don't refactor code unnecessarily

### Success Criteria

You're doing well when:
- Changes are minimal and focused
- Tests pass consistently
- Code follows project conventions
- Commits are clear and atomic
- No security issues introduced
- Work is well-organized and tracked
- User requirements are met precisely

---

## Appendix

### Useful Commands Reference

**Git**:
```bash
git status                           # Check working tree status
git branch -a                        # List all branches
git fetch origin                     # Fetch remote changes
git log --oneline -n 10             # View recent commits
git diff                             # View unstaged changes
git diff --staged                    # View staged changes
```

**Project-Specific** (to be added):
```bash
# Build commands
# Test commands
# Linting commands
# Deployment commands
```

### Resources

- [Project README](./README.md) (to be created)
- [Contributing Guidelines](./CONTRIBUTING.md) (if applicable)
- [Code of Conduct](./CODE_OF_CONDUCT.md) (if applicable)

---

**Last Updated**: 2026-01-22
**Maintained By**: AI Assistants working on this project
**Status**: Living document - update as project evolves
