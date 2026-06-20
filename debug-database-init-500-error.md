# Debug Session: database-init-500-error

## Status: [OPEN]

## Symptom
- `Failed to initialize database: AxiosError: Request failed with status code 500`
- `loadStatistics` also fails with 500
- Location: `quiz.js:41` (initDatabase) and `quiz.js:317` (loadStatistics)

## Environment
- Frontend: http://localhost:3001
- Backend: http://154.201.94.140 (deployed server)
- API endpoint returning 500

## Hypotheses
1. **Backend database not initialized** - The server may not have the required database tables/columns
2. **Backend route handler throws exception** - The `/api/init-db` or statistics endpoint has a bug
3. **Missing database file** - The `quiz_system.db` file is missing on the server
4. **Permission issue** - The backend cannot write to the database file location
5. **Flask app crashed** - The backend process may have crashed after deployment

## Next Steps
- Add instrumentation to backend to capture the actual error
- Check backend logs for stack trace
