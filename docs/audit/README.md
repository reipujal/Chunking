# Audit Board — SAP SD Knowledge Base

Ejecutar: `/audit-board docs/audit/audit_board_profile.md`
(Si el skill `/audit-board` no está instalado, el profile v2.0 es autónomo: pásalo como prompt a un LLM auditor.)

## Cuándo ejecutar

| Trigger | Tier |
|---------|------|
| Tras cada documento procesado | Quick (ROL 0, 2, 4, 6, 10) |
| ≥3 documentos nuevos o mensual | Standard (ROL 0, 1, 2, 4, 5, 6, 7, 9, 10, 16) |
| Trimestral o antes de RAG producción | Full (ROL 0, 1–12, 16 + síntesis) |

> **ROL 0 (pre-vuelo, bloqueante)** obligatorio en todos los tiers: si el corpus no es auditable
> (validador roto, índice desincronizado, git con lock) el audit se detiene ahí.
> **ROL 16 (meta-audit)** re-verifica que las correcciones declaradas se aplicaron de verdad.
> Toda auditoría **cierra** con síntesis + regeneración de `audit_context_shared.md` (REGLA 11).

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `audit_board_profile.md` | 14 roles (incl. ROL 0 pre-vuelo y ROL 16 meta-audit), clusters, debates, tiers |
| `audit_context_shared.md` | Estado del corpus — regenerar desde disco antes de cada audit |
| `analisis_critico_independiente_2026-06-07.md` | Análisis adversario independiente (base de la v2.0) |
| `results/` | Outputs históricos de cada auditoría |
