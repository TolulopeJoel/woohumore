# WooHumore Documentation

## Project Description
WooHumore is an API that finds positive news stories online and turns them into interesting videos automatically. This project gives people a refreshing break from typical news that are usually sad and depressing by focusing on positive stories.

## Motivation
Every day, we’re surrounded by negative news, which can be overwhelming. I created WooHumore to bring more balance by focusing on positive stories that uplifts people. This project gives people a break from the negativity and uses automation to deliver inspiring video content to a wider audience.


## Features
- Automated news scraping from multiple sources
- NLP-powered content summarization
- Text-to-speech conversion
- Automated video generation
- Content management system
- Subscriber management
- API-first architecture
- Cloud storage integration
- Multiple image service integrations

## Quick Start

Visit the [website](https://woohumore.netlify.app) (under construction) to check some generated news.


## Usage

### API Endpoints
The API provides several endpoints for managing content:

#### Posts
- `GET /posts/` - List published posts
- `GET /posts/<id>/` - Get post details
- `GET /posts/summarise/` - Summarize posts
- `GET /posts/sources/` - List active news sources

#### News
- `GET /news/` - List published news videos
- `POST /news/create/` - Create new video

#### Scraper
- `POST /scraper/posts-list/` - Scrape new posts
- `GET /scraper/posts-detail/` - Get post details

#### Videos
- `POST /videos/add-audio/` - Add audio to posts

#### Subscribers
- `GET /subscribers/` - List subscribers
- `POST /subscribers/` - Add new subscriber

### API Documentation
- `/docs/` - Swagger UI documentation
- `/` - OpenAPI schema

## Ongoing Enhancements
- Additional news source integrations
- Fine-tuning a large language model (LLM) to highlight positive aspects within negative news stories.

## Future Enhancements
- Advanced video generation features

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feat-branch-name`
3. Make your changes and commit them: `git commit -m 'Update some feature'`
4. Push to the branch: `git push origin feat-branch-name`
5. Submit a pull request

## License
The WooHumore API is released under the [MIT License](LICENSE).

## Contact
For issues or suggestions, please contact the developer (Tolu) at dotolulope2@gmail.com or visit the GitHub repository.
