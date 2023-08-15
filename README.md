# actions
Reusable GitHub actions and workflows.

## Workflows

### lint-python.yml

Our python linting checks. Configurable

### poetry-publish.yml

Automatically build and publish a poetry package to our private Google Artifact Registry.
Compatible with repos based on our `scene-connect/zuos-python-package-template`.

Features:
- Checks for relevant changes.
- Automatically bump the package version by prefixing the PR title with:
  - Patch, Minor, Major
  - Automatically bumps version patch leve for `dependabot` PRs.
- Builds the package to check everything works.
- Checks if the (bumped) package version already exists in the Artifact Registry
  (you'll have to set your own version to resolve conflicts)
- Publishes the package on merge to main.

## Actions

### install-system-dependencies

A simple action to install system/os level dependencies (using `apt-get`).

### python-package-manager

Common actions for performing actions with a variety of python package managers.
Actions in here mostly use sub-actions to perform the task with different package
managers, and an overall action to switch on a `package-manager` input.

#### install-dependencies

Install a project's dependencies for CI workflows.

#### run-command

Run a command, within the project venv set up by `install-dependences`.
Useful in shared actions which themselves use a `package-manager` input.
