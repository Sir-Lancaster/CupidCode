# WORKING STARTER CODE INSTALLATION STEPS:
1. Ensure you have python, poetry, node, and npm installed globally
2. Run `git clone [path to the repo]`
3. Run `cd Code/`
4. Run `poetry shell`
5. Run `poetry install`
6. Run `cd server/`
7. Run `python manage.py migrate`
8. Run `touch .env`
9. Run `code .env` (or open the file in whichever text editor you like)
10. Reference .env.example for what is required in your .env, it is located [here](server/.env.example)
11. Run `python manage.py runserver`
12. Open a new terminal tab and navigate to project root
13. Run `cd Code/`
14. Run `poetry shell`
15. Run `cd client/`
16. Run `npm install`
17. Run `npm audit fix` (This won't fix all of the vulnerabilities but at least some)
18. Run `npm run dev`
19. Visit `http://localhost:8000`


Additionally, some information about what else you might need:
an Account for an api key for Google Maps, Twilio, Paypal, and OpenAI

We deployed to the cloud using Microsoft Azure, we used default settings and made sure ports 80 and 443, for HTTP and HTTPs traffic respectively. You will have to find a third party app to get a valid URL from, we used https://www.noip.com/login?ref_url=console

On GitLab you will need to set up CI/CD environment variables for the public and private keys in order for the [YAML](../.gitlab-ci.yml) file to work. The deploy scripts folder is used by the YAML.