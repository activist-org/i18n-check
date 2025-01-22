<div align="center">
  <a href="https://github.com/activist-org/i18n-check"><img src="https://raw.githubusercontent.com/activist-org/i18n-check/main/.github/resources/i18nCheckGitHubBanner.png" width=1024 alt="i18n check logo"></a>
</div>

[![issues](https://img.shields.io/github/issues/activist-org/i18n-check?label=%20&logo=github)](https://github.com/activist-org/i18n-check/issues)
[![python](https://img.shields.io/badge/Python-4B8BBE.svg?logo=python&logoColor=ffffff)](https://github.com/activist-org/i18n-check/blob/main/CONTRIBUTING.md)
[![pypi](https://img.shields.io/pypi/v/i18n-check.svg?label=%20&color=4B8BBE)](https://pypi.org/project/i18n-check/)
[![pypistatus](https://img.shields.io/pypi/status/i18n-check.svg?label=%20)](https://pypi.org/project/i18n-check/)
[![license](https://img.shields.io/github/license/activist-org/i18n-check.svg?label=%20)](https://github.com/activist-org/i18n-check/blob/main/LICENSE.txt)
[![coc](https://img.shields.io/badge/Contributor%20Covenant-ff69b4.svg)](https://github.com/activist-org/i18n-check/blob/main/.github/CODE_OF_CONDUCT.md)
[![matrix](https://img.shields.io/badge/Matrix-000000.svg?logo=matrix&logoColor=ffffff)](https://matrix.to/#/#activist_community:matrix.org)

### Check i18n/L10n keys and values

`i18n-check` is a Python package to automate the validation of keys and values of your internationalization and localization processes.

Developed by the [activist community](https://github.com/activist-org), this process is meant to assure that development and i18n/L10n teams are in sync when using JSON based localization processes. The action can be expanded later to work for other file type processes as needed.

> [!NOTE]
> For the GitHub action please see [activist-org/i18n-check-action](https://github.com/activist-org/i18n-check-action).

<a id="contents"></a>

# **Contents**

- [Conventions](#contentions)
- [How it works](#how-it-works)
- [Configuration](#configuration)
- [Contributors](#contributors)

<a id="conventions"></a>

# Conventions [`⇧`](#contents)

[activist](https://github.com/activist-org/activist) i18n keys follow the following conventions that are enforced by `i18n-check`:

- All key base paths should be the file path where the key is used
- If a key is used in more than one file, then the lowest common directory followed by `_global` is the base path
- Base paths should be followed by a minimally descriptive content reference
  - Only the formatting of these content references is checked via `i18n-check`
- Separate base directory paths by periods (`.`)
- Separate all directory and file name components as well as content references by underscores (`_`)
- Repeat words in file paths for sub directory organization should not be repeated in the key

> [!NOTE]
> An example valid key is:
>
> Key: `"components.component_name.CONTENT_REFERENCE"`
>
> File: `components/component/ComponentName.ext`

<a id="how-it-works"></a>

# How it works [`⇧`](#contents)

You provide `i18n-check` with the following arguments:

- `src-dir`: The path to the directory that has source code to check
- `i18n-dir`: The directory path to your i18n files
- `i18n-src`: The name of the i18n source file
- `i18n-map`: The path to the i18n-map file (optional - see below)

From there the following checks are ran across your codebase:

- `key_identifiers`: Does the source file have keys that don't match the above format or name conventions?
  - Rename them so i18n key usage is consistent and their scope is communicated in their name.
- `unused_keys`: Does the source file have keys that are not used in the codebase?
  - Remove them so the localization team isn't working on strings that aren't used.
- `non_source_keys`: Do the target locale files have keys that are not in the source file?
  - Remove them as they won't be used in the application.
- `repeat_values`: Does the source file have repeat values that can be combined into a single key?
  - Combine them so the localization team only needs to localize one of them.

Each of the above checks is ran in parallel with directions for how to fix the i18n files being provided when errors are raised. Checks can also be disabled in the workflow via options passed in the YAML file.

`i18n-check` can also generate an `i18nMap` object from the `i18n-src` file that can be used to load in i18n keys. Methods within this object map to keys within the source file as in the following example:

```ts
// _global.hello_global would be a key in our i18n-src file.
export const i18nMap = {
  _global: {
    hello_global: "_global.hello_global",
  },
};
```

The map is then used in files in the following way:

```ts
// Using vue-i18n:
const hello_global_i18n_scope = i18n.t(i18nMap._global.hello_global);
```

Using `i18nMap` allows development teams to check the existence of all i18n keys used in the codebase as linting will detect that keys don't exist on the object. The package will check that `i18nMap` is up to date with the `i18n-src` file if this functionality is enabled in the configuration file.

<a id="configuration"></a>

# Configuration [`⇧`](#contents)

The following details the `.18n-check.yaml` configuration file for `i18n-check`, with a further example being the [configuration file for this repository](/.i18n-check-config.yaml) that we use in testing.

```yaml
src-dir: frontend
i18n-dir: frontend/i18n
i18n-src: frontend/i18n/en.json
i18n-map: frontend/types/i18n-map.ts
```

<a id="contributors"></a>

# Contributors [`⇧`](#contents)

Thanks to all our amazing [contributors](https://github.com/activist-org/i18n-check/graphs/contributors)! ❤️

<a href="https://github.com/activist-org/i18n-check/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=activist-org/i18n-check" />
</a>
