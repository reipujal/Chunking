# Audit Board — SAP SD Knowledge Base

Ejecutar: `/audit-board docs/audit/audit_board_profile.md`

## Cuándo ejecutar

| Trigger | Tier |
|---------|------|
| Tras cada documento procesado | Quick (ROL 2, 4, 6, 10) |
| ≥3 documentos nuevos o mensual | Standard (ROL 1,2,4,5,6,7,9,10) |
| Trimestral o antes de RAG producción | Full (ROL 1–12 + síntesis) |

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `audit_board_profile.md` | 12 roles, 5 clusters, 2 debates, tiers |
| `audit_context_shared.md` | Estado del corpus — regenerar antes de cada audit |
| `results/` | Outputs históricos de cada auditoría |
