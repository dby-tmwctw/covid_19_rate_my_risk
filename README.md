# COVID-19 Know-My-Risk

## Inspiration
During the pandemic, people, especially the youth, might be over-confident about their risk contracting COVID-19. On the other hand, those who are concerned might have difficulties gauging precisely their risk. School and workplaces might want to know whether some students/employees have high risks of COVID. Hence, our app tries to provide a way to easily access a person's level of concern regarding COVID-19.

## What it does
- On login, a person fill in some personal information, and the app gives an initial screening about a person's risk score (higher means more dangerous)
- After signing up, one can log in to his/her account and record everyday activities. The score will fluctuate according to that, reflecting real-time changes of one's risk score

## How we built it
Our project is divided into three parts:
### Data Collection and processing
We collect data from trusted sources in the two main fields below:
- Location and COVID-19. Those who live in areas that are susceptible to disease outbreak (assessed from CDC's SVI data), and those whose area has a higerh percentage of positive rate have higher risks of contracting COVID-19
- Personal preconditions and symptoms. We collect data about one's preconditions, symptoms, and whether they are tested positive for COVID to train machine learning data. The model will then tell us a person's risks of contracting COVID-19 based on this information

### Back-end implementation
With the data we collected, we then build our back-end.
- Regarding location, we use the person's zip-code and consider both the district's SVI and positive rate to generate a score representing the person's location score
- Regarding personal precondition and symptoms, we use the person's response to form a response vector. This vector is fed into two machine learning models based on Logistic Regression, generating a score to assess one's personal risk
- Dynamic data is an ongoing task of our app, which probably won't be full-fledged until many people uses our app. Our current implementation relies on users filling in information about the places they visited, and we use that to calculate a real-time score based on the person's original score. If enough people use our data, we can relate this tracking data with one's COVID-19 testing result. The resulting dataset can be fed into a machine learning model, and be made publicly available (personal information removed) to contribute to COVID-19 research

### Front-end implementation and pipelining

We build a web app with React as front end from scratch. The front-end communicates with the back-end with Flask, and the data that transmitted back and forth are JSON. We deployed our server on Heruko.

## Challenges we ran into
### Data
- The datasets we collected is not clean
- Many datasets are either aggregated data or does not contain information about whether the patient is tested positive
- Datasets are huge, making search time slow

### Implementations
- Communication between back-end and front-end proves to be difficult, especially when it is across different platform
- Machine learning models do not converge on indicators that are less strong, such as preconditions
- Deciding on a suitable model suitable to our scoring scheme

## Accomplishments that we're proud of
- Successfully aggregated all datasets and considerations to generate a differentiating and reliable score
- Search time is really short, get your result instantly
- Successfully combined front end and back-end to produce a working web application

## What we learned
- Data analysis tools and models
- Machine learning integration
- React framework and Flask

## What's next for COVID-19 Know-My-Risk
With our static scoring ready, we can focus on dynamic scoring that reflects one's real data. A person can simply place pins on Google maps, and we analyze risks for visiting that place automatically. Daily activities like greeting friends, or eating out can also be factored in. After one sign in, a person can build his own historical record of daily risks. The person can use this to track his possibilities of getting COVID-19 and adjust life plans accordingly. With enough people using our app, we can use the tracking data to do further predictions on one's risks, and the data itself is valuable for COVID-19 research.
