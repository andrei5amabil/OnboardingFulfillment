Requirements: 
  1. uv python package manager: https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1
  2. FastAPI: https://fastapi.tiangolo.com/#requirements
  3. supabase: https://supabase.com/docs/reference/javascript/installing

After installing run:
  -uv add supabase python-dotenv
  -npm install supabase --save-dev
  -npx supabase init (daca nu merge adaugati --force)
  -npx supabase start
  -uv run fastapi dev
  
Create .env file and add: 
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_KEY=<Publishable Authentication Key>    // npx supabase status -> Authentication Keys
SUPABASE_SECRET_KEY=<Secret Authentication Key>  // 

http://127.0.0.1:54323/project/default -> supabase web interface
http://127.0.0.1:8000/docs -> FastAPI SwaggerUI pentru testare endpoints
