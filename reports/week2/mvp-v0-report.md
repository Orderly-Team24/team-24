# MVP v0 Report

## Purpose and Description of MVP v0

Orderly is a web application prototype that helps users choose a meal based on dietary preferences and budget constraints.

The purpose of MVP v0 is to provide a runnable web application that demonstrates the core user flow:

* entering food allergies;
* selecting a food preference;
* setting a budget;
* receiving a dish recommendation.

User data is stored locally using browser localStorage.

## Deployment URL

https://keen-pegasus-a95a6a.netlify.app/

## Public Video Demonstration

https://youtu.be/CKgT0l3MgDk?si=0FWBhFiLGvoZRtDo

## Relationship to the Prototype and Proposed MVP v1 Stories

The MVP v0 implementation follows the user flow demonstrated in the prototype.

The future MVP v1 is planned to include:

* menu image upload;
* menu text extraction;
* AI-based dish recommendation;
* personalized meal selection.

MVP v0 serves as the initial technical foundation for these future features.

## Current Limitations, Placeholders, and Mocks

Current limitations include:

* recommendation data is hardcoded;
* dish name is a placeholder;
* dish price is a placeholder;
* no backend service;
* no database;
* no menu image processing;
* no AI recommendation engine.

The current version is intended to demonstrate navigation and interaction flow only.

## Local Setup Instructions

1. Clone the repository.

```bash
git clone https://github.com/rxxtzz/team-24.git
```

2. Open the project folder.

3. Run a local web server:

```bash
python -m http.server 8000
```

4. Open:

```text
http://localhost:8000
```

Alternatively, open index.html directly in a browser.

## Smoke Check Scenario

### Access

Open the application using:

https://keen-pegasus-a95a6a.netlify.app/

### Steps

1. Enter an allergy (for example: peanuts).
2. Select a food preference.
3. Click "Continue".
4. Enter a budget value.
5. Click "Upload Menu Photo".
6. Verify that the recommendation page opens.
7. Click any recommendation button.

### Expected Results

* The application loads successfully.
* Navigation between pages works.
* User input is saved in localStorage.
* The recommendation page is displayed.
* Interactive buttons respond to user actions.

This smoke check confirms that MVP v0 is accessible and usable for its demonstrated purpose.
