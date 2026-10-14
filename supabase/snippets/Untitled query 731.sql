-- 1. Add rich product metadata columns to software_products
ALTER TABLE public.software_products
ADD COLUMN IF NOT EXISTS description TEXT,
ADD COLUMN IF NOT EXISTS access_url TEXT,
ADD COLUMN IF NOT EXISTS docs_url TEXT;

-- 2. Populate descriptive metadata, SSO access points, and official guides
UPDATE public.software_products
SET
  description = CASE
    WHEN name ILIKE '%datagrip%' THEN 'Cross-platform multi-engine IDE for querying, schema exploration, and database management.'
    WHEN name ILIKE '%jetbrains%' OR name ILIKE '%pycharm%' OR name ILIKE '%intellij%' THEN 'Full-featured enterprise IDE with intelligent code analysis, debugging, and testing.'
    WHEN name ILIKE '%powerbi%' THEN 'Interactive business intelligence and dashboard reporting tool for data analysis.'
    WHEN name ILIKE '%google%' OR name ILIKE '%workspace%' THEN 'Core enterprise collaboration suite including Gmail, Drive, Calendar, and Meet.'
    WHEN name ILIKE '%365%' OR name ILIKE '%office%' THEN 'Microsoft cloud productivity suite for documents, spreadsheets, and team collaboration.'
    WHEN name ILIKE '%jira%' THEN 'Issue tracking and project management platform for sprint planning and tickets.'
    WHEN name ILIKE '%slack%' THEN 'Centralized workspace communication and team messaging channels.'
    WHEN name ILIKE '%github%' THEN 'Source code management, pull request reviews, and CI/CD automation pipelines.'
    WHEN name ILIKE '%aws%' THEN 'Cloud infrastructure platform, compute services, and IAM portal.'
    WHEN name ILIKE '%docker%' THEN 'Containerized local development runtime and image management.'
    ELSE COALESCE(description, 'Enterprise software license provisioned and maintained by IT Operations.')
  END,
  access_url = CASE
    WHEN name ILIKE '%datagrip%' OR name ILIKE '%jetbrains%' THEN 'https://account.jetbrains.com/'
    WHEN name ILIKE '%powerbi%' THEN 'https://app.powerbi.com/'
    WHEN name ILIKE '%google%' OR name ILIKE '%workspace%' THEN 'https://workspace.google.com/'
    WHEN name ILIKE '%365%' OR name ILIKE '%office%' THEN 'https://portal.office.com/'
    WHEN name ILIKE '%jira%' THEN 'https://id.atlassian.com/'
    WHEN name ILIKE '%slack%' THEN 'https://slack.com/signin'
    WHEN name ILIKE '%github%' THEN 'https://github.com/login'
    WHEN name ILIKE '%aws%' THEN 'https://aws.amazon.com/console/'
    WHEN name ILIKE '%docker%' THEN 'https://hub.docker.com/'
    ELSE COALESCE(access_url, 'https://sso.atossoftware.com')
  END,
  docs_url = CASE
    WHEN name ILIKE '%datagrip%' THEN 'https://www.jetbrains.com/help/datagrip/'
    WHEN name ILIKE '%jetbrains%' THEN 'https://www.jetbrains.com/help/'
    WHEN name ILIKE '%powerbi%' THEN 'https://learn.microsoft.com/en-us/power-bi/'
    WHEN name ILIKE '%google%' OR name ILIKE '%workspace%' THEN 'https://support.google.com/a/'
    WHEN name ILIKE '%365%' OR name ILIKE '%office%' THEN 'https://support.microsoft.com/office'
    WHEN name ILIKE '%jira%' THEN 'https://support.atlassian.com/jira-software-cloud/'
    WHEN name ILIKE '%slack%' THEN 'https://slack.com/help'
    WHEN name ILIKE '%github%' THEN 'https://docs.github.com/'
    WHEN name ILIKE '%aws%' THEN 'https://docs.aws.amazon.com/'
    WHEN name ILIKE '%docker%' THEN 'https://docs.docker.com/'
    ELSE COALESCE(docs_url, 'https://wiki.atossoftware.com/it/onboarding')
  END
WHERE description IS NULL OR access_url IS NULL OR docs_url IS NULL;

-- 3. Verify the changes
SELECT product_id, name, vendor, license_type, access_url, docs_url, description
FROM public.software_products;