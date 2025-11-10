# Publishing to PyPI

This guide provides instructions for publishing `pypsa-explorer` to the Python Package Index (PyPI).

## Prerequisites

1. **PyPI Account**: Create accounts on both [PyPI](https://pypi.org/account/register/) and [TestPyPI](https://test.pypi.org/account/register/)
2. **API Tokens**: Generate API tokens for secure authentication:
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/
3. **Build Tools**: Install build and twine (already done in this project)
   ```bash
   uv pip install build twine
   ```

## Configuration

### Configure PyPI Credentials

Store your API tokens securely in `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PYPI_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

Set proper permissions:
```bash
chmod 600 ~/.pypirc
```

## Pre-Publishing Checklist

Before publishing, ensure:

- [ ] Version number is updated in `pyproject.toml`
- [ ] CHANGELOG.md is updated with release notes
- [ ] All tests pass: `uv run pytest`
- [ ] Code is properly formatted: `ruff format . && ruff check .`
- [ ] Type checks pass: `mypy src/`
- [ ] Git branch is clean (all changes committed)
- [ ] README.md is up to date

## Build the Package

1. **Clean previous builds**:
   ```bash
   rm -rf dist/ build/ src/*.egg-info
   ```

2. **Build the distribution packages**:
   ```bash
   uv run python -m build
   ```

   This creates:
   - `dist/pypsa_explorer-VERSION-py3-none-any.whl` (wheel package)
   - `dist/pypsa_explorer-VERSION.tar.gz` (source distribution)

3. **Verify the build**:
   ```bash
   uv run twine check dist/*
   ```

   You should see:
   ```
   Checking dist/pypsa_explorer-VERSION-py3-none-any.whl: PASSED
   Checking dist/pypsa_explorer-VERSION.tar.gz: PASSED
   ```

## Publishing Process

### Step 1: Test on TestPyPI (Recommended)

First, publish to TestPyPI to verify everything works:

```bash
uv run twine upload --repository testpypi dist/*
```

Test the installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pypsa-explorer
```

Note: The `--extra-index-url` is needed because dependencies may not be on TestPyPI.

### Step 2: Publish to PyPI

Once verified on TestPyPI, publish to the official PyPI:

```bash
uv run twine upload dist/*
```

You'll see output like:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading pypsa_explorer-0.1.0-py3-none-any.whl
Uploading pypsa_explorer-0.1.0.tar.gz
```

### Step 3: Verify Installation

Test that users can install your package:

```bash
pip install pypsa-explorer
```

## Version Management

### Updating the Version

Update the version in `pyproject.toml`:

```toml
[project]
version = "0.2.0"  # Update this
```

Follow [Semantic Versioning](https://semver.org/):
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes

### Creating a Release

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit changes:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 0.2.0"
   ```
4. Create a git tag:
   ```bash
   git tag -a v0.2.0 -m "Release version 0.2.0"
   git push origin v0.2.0
   ```
5. Build and publish (see above)

## CI/CD Automation (Optional)

The repository includes `.github/workflows/publish.yml` for automated publishing via GitHub Actions.

To enable:

1. Add PyPI API token to GitHub Secrets:
   - Go to repository Settings → Secrets → Actions
   - Add secret named `PYPI_API_TOKEN`

2. Create a new release on GitHub:
   - Go to Releases → Create new release
   - Create a tag (e.g., `v0.2.0`)
   - Publish the release

The workflow will automatically build and publish to PyPI.

## Troubleshooting

### Common Issues

**File already exists on PyPI**:
- Each version can only be uploaded once
- Increment the version number and rebuild

**Invalid credentials**:
- Verify your API token in `~/.pypirc`
- Ensure token has upload permissions

**Package name already taken**:
- Choose a different name in `pyproject.toml`
- Check availability: https://pypi.org/project/YOUR-PACKAGE-NAME/

**Large package size**:
- The demo-network.nc file is 50MB and is included in the distribution
- Consider excluding it from the wheel in future versions if size becomes an issue
- Users can download their own network files

### Validation Errors

If `twine check` fails:
- Ensure README.md is valid markdown
- Check that all required metadata is in `pyproject.toml`
- Verify LICENSE file exists

## Important Notes

### PyPSA Dependency

The package depends on PyPSA from GitHub:
```toml
"pypsa @ git+https://github.com/PyPSA/PyPSA.git@master"
```

This is supported by modern pip versions but users will need:
- Git installed on their system
- Internet connection during installation

If this causes issues, consider switching to a released PyPSA version on PyPI when available.

### Demo Network File

The package includes a 50MB demo network file (`demo-network.nc`). This is intentional for out-of-the-box functionality, but be aware:
- PyPI has a 100MB file size limit (we're within limits)
- Download times may be longer for users
- Consider providing alternative download methods for larger networks

## Post-Publishing

After successful publication:

1. **Update README badges**: Verify PyPI badge shows correct version
2. **Announce the release**:
   - Update project documentation
   - Post on relevant forums/communities
   - Update PyPSA ecosystem listings
3. **Monitor issues**: Watch for installation problems
4. **Documentation**: Ensure readthedocs.io is updated (if configured)

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
- [PEP 440 - Version Identification](https://peps.python.org/pep-0440/)
