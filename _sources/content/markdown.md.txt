# Markdown examples

## Footnotes

```markdown
- This is a manually-numbered footnote reference.[^3]
- This is an auto-numbered footnote reference.[^myref]

[^myref]: This is an auto-numbered footnote definition.
[^3]: This is a manually-numbered footnote definition.
```

Here is a footnote.[^footnote]

[^footnote]: will appear at the bottom of the page.

## Roles

```markdown
{rolename}`role content`
```

```markdown
{doc}`This <about>` is a reference to another document.
```

{doc}`This <about>` is a reference to another document

```markdown
It is also possible to make a {doc}`custom named <about>` link as a reference.
```

It is also possible to make a {doc}`custom named <about>` link as a reference.

```markdown
{sub-ref}`today` | {sub-ref}`wordcount-words` words | {sub-ref}`wordcount-minutes` min read
```

{sub-ref}`today` | {sub-ref}`wordcount-words` words | {sub-ref}`wordcount-minutes` min read

% some comment which will not be shown