# Permission Mirroring Design

## Principle

AI can only access or act on what the requesting user is allowed to access or do.

## Required checks

1. user identity  
2. workspace  
3. role  
4. data permissions  
5. tool permissions  
6. action permissions  
7. approval requirement  

## Example

If a sales user cannot see finance documents, KnowledgeAgent cannot use finance documents in an answer for that user.

## Implementation idea

Every AI run receives:

- user_id  
- workspace_id  
- role  
- allowed_source_ids  
- allowed_tool_ids  
- allowed_action_classes  

---

## API shape (later)

```text
POST /governance/permission-check
{
  "user_id": "...",
  "workspace_id": "...",
  "agent_id": "...",
  "requested_sources": [],
  "requested_action": "draft_email"
}
```

See also: [`PERMISSION_MIRRORING.md`](../governance/PERMISSION_MIRRORING.md).
