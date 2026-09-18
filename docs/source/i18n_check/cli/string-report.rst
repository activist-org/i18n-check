Potentially untranslated strings report
=======================================

The string report should identify source strings that have no localized value,
show the source file and key, and leave files unchanged. A machine-readable
mode should be stable enough for CI while the default output remains readable
for a contributor fixing translations.

When implementing the command requested in issue 120, cover an empty catalog,
a fully translated catalog, and a source string with a missing locale value.
