## Image Scraper Deployment

### Steps
1. Push code to github
2. Create: Web App
```
* Create/Select: Resource
* Create: Instance name
* Select; Runtime stack
* Review + Create
* Goto: Deployment
    * Continious Dep: Enable
```
* yml file auto created by Azure for deployment
    * .github/workflows/tproj-image_scrap_deploy_image-scrap.yml
    * Delete this if want to deploy again