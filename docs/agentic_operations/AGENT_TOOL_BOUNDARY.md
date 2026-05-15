# Agent Tool Boundary

## تصنيف الأدوات (Class A–F)

| Class | النوع | MVP |
|-------|--------|-----|
| A | Read-only | مسموح |
| B | Analysis | مسموح |
| C | Draft generation | مسموح |
| D | Internal write | **بموافقة** |
| E | External action | **محظور في MVP** |
| F | High-risk | **ممنوع** |

## القاعدة

**Agents may prepare external actions. Agents may not execute external actions in MVP.**

## الكود

`agent_permissions.py` — `ToolClass`, `tool_class_allowed_in_mvp`.
