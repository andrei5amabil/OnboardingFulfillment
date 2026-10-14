-- 1. Update all known software products to their authentic live portals and docs
UPDATE public.software_products
SET
  access_url = CASE
    -- JetBrains Products
    WHEN name ILIKE '%datagrip%' THEN 'https://www.jetbrains.com/datagrip/'
    WHEN name ILIKE '%pycharm%' THEN 'https://www.jetbrains.com/pycharm/'
    WHEN name ILIKE '%intellij%' THEN 'https://www.jetbrains.com/idea/'
    WHEN name ILIKE '%webstorm%' THEN 'https://www.jetbrains.com/webstorm/'
    WHEN name ILIKE '%jetbrains%' THEN 'https://account.jetbrains.com/'

    -- Microsoft / Office / Power BI
    WHEN name ILIKE '%powerbi%' OR name ILIKE '%power bi%' THEN 'https://app.powerbi.com/'
    WHEN name ILIKE '%teams%' THEN 'https://teams.microsoft.com/'
    WHEN name ILIKE '%365%' OR name ILIKE '%office%' OR name ILIKE '%excel%' OR name ILIKE '%word%' THEN 'https://www.office.com/'

    -- Google Workspace / Collaboration
    WHEN name ILIKE '%google%' OR name ILIKE '%workspace%' OR name ILIKE '%gmail%' THEN 'https://workspace.google.com/'

    -- Atlassian
    WHEN name ILIKE '%jira%' THEN 'https://www.atlassian.com/software/jira'
    WHEN name ILIKE '%confluence%' THEN 'https://www.atlassian.com/software/confluence'
    WHEN name ILIKE '%trello%' THEN 'https://trello.com/login'

    -- Developer & Cloud Tools
    WHEN name ILIKE '%github%' THEN 'https://github.com/login'
    WHEN name ILIKE '%gitlab%' THEN 'https://gitlab.com/users/sign_in'
    WHEN name ILIKE '%docker%' THEN 'https://hub.docker.com/'
    WHEN name ILIKE '%postman%' THEN 'https://web.postman.co/'
    WHEN name ILIKE '%aws%' THEN 'https://aws.amazon.com/console/'
    WHEN name ILIKE '%azure%' THEN 'https://portal.azure.com/'
    WHEN name ILIKE '%gcp%' OR name ILIKE '%cloud%' THEN 'https://console.cloud.google.com/'
    WHEN name ILIKE '%slack%' THEN 'https://slack.com/signin'
    WHEN name ILIKE '%figma%' THEN 'https://www.figma.com/login'
    WHEN name ILIKE '%notion%' THEN 'https://www.notion.so/login'
    WHEN name ILIKE '%zoom%' THEN 'https://zoom.us/signin'
    WHEN name ILIKE '%vpn%' OR name ILIKE '%tailscale%' THEN 'https://tailscale.com/'
    WHEN name ILIKE '%1password%' OR name ILIKE '%password%' THEN 'https://1password.com/'

    -- Fallback: If it still contains 'atossoftware' or is empty, link to Google Workspace login
    WHEN access_url ILIKE '%atossoftware%' OR access_url IS NULL OR access_url = '' THEN 'https://workspace.google.com/'
    ELSE access_url
  END,

  docs_url = CASE
    -- JetBrains Docs
    WHEN name ILIKE '%datagrip%' THEN 'https://www.jetbrains.com/help/datagrip/'
    WHEN name ILIKE '%pycharm%' THEN 'https://www.jetbrains.com/help/pycharm/'
    WHEN name ILIKE '%intellij%' THEN 'https://www.jetbrains.com/help/idea/'
    WHEN name ILIKE '%jetbrains%' THEN 'https://www.jetbrains.com/help/'

    -- Microsoft Docs
    WHEN name ILIKE '%powerbi%' OR name ILIKE '%power bi%' THEN 'https://learn.microsoft.com/en-us/power-bi/'
    WHEN name ILIKE '%teams%' THEN 'https://support.microsoft.com/teams'
    WHEN name ILIKE '%365%' OR name ILIKE '%office%' THEN 'https://support.microsoft.com/office'

    -- Google Docs
    WHEN name ILIKE '%google%' OR name ILIKE '%workspace%' OR name ILIKE '%gmail%' THEN 'https://support.google.com/a/users/'

    -- Atlassian Docs
    WHEN name ILIKE '%jira%' THEN 'https://support.atlassian.com/jira-software-cloud/'
    WHEN name ILIKE '%confluence%' THEN 'https://support.atlassian.com/confluence-cloud/'

    -- Developer & Cloud Docs
    WHEN name ILIKE '%github%' THEN 'https://docs.github.com/'
    WHEN name ILIKE '%gitlab%' THEN 'https://docs.gitlab.com/'
    WHEN name ILIKE '%docker%' THEN 'https://docs.docker.com/'
    WHEN name ILIKE '%postman%' THEN 'https://learning.postman.com/docs/'
    WHEN name ILIKE '%aws%' THEN 'https://docs.aws.amazon.com/'
    WHEN name ILIKE '%azure%' THEN 'https://learn.microsoft.com/en-us/azure/'
    WHEN name ILIKE '%slack%' THEN 'https://slack.com/help'
    WHEN name ILIKE '%figma%' THEN 'https://help.figma.com/'
    WHEN name ILIKE '%notion%' THEN 'https://www.notion.so/help'
    WHEN name ILIKE '%zoom%' THEN 'https://support.zoom.us/'
    WHEN name ILIKE '%vpn%' OR name ILIKE '%tailscale%' THEN 'https://tailscale.com/kb/'
    WHEN name ILIKE '%1password%' OR name ILIKE '%password%' THEN 'https://support.1password.com/'

    -- Fallback: If it still contains 'atossoftware' or is empty, link to official user docs
    WHEN docs_url ILIKE '%atossoftware%' OR docs_url IS NULL OR docs_url = '' THEN 'https://support.google.com/'
    ELSE docs_url
  END;

-- 2. Safety purge: Check and force-replace any remaining atossoftware link
UPDATE public.software_products
SET access_url = 'https://workspace.google.com/'
WHERE access_url ILIKE '%atossoftware%';

UPDATE public.software_products
SET docs_url = 'https://support.google.com/'
WHERE docs_url ILIKE '%atossoftware%';

-- 3. Verify: Review your entire software catalog and confirm 0 atossoftware links remain
SELECT product_id, name, vendor, access_url, docs_url
FROM public.software_products
ORDER BY name ASC;