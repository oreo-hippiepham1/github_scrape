import praw
import pandas as pd

# Reddit API credentials
client_id = 'CIkYw772eXWYno3Z-dfGhA'
client_secret = 'Bysc7gRHKdRo2f4IQrKN4flPt6G1tA'
user_agent = 'Reddit scraper (by u/HippiePham_01)'

# Initialize the Reddit API client
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


# Function to scrape comments from a post
def scrape_comments(subreddit, post_id, df, limit=100):
    # Fetch the post using its ID
    post = reddit.submission(id=post_id)

    # Enable comments if not already enabled
    post.comments.replace_more(limit=None)

    # Extract post information
    post_title = post.title
    post_upvotes = post.score
    post_link = post.url

    # Scrape comments
    count = 0
    for comment in post.comments.list():
        if isinstance(comment, praw.models.Comment):
            cmt = comment.body if comment.body else 'None'
            cmt_upvotes = comment.score if comment.score else 'None'
            # Append comment information to DF
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            'subreddit': [subreddit],
                            'post_title': [post_title],
                            'post_upvotes': [post_upvotes],
                            'post_link': [post_link],
                            'comment': [cmt],
                            'comment_upvotes': [cmt_upvotes]
                        }
                    ),
                ],
                ignore_index=True,
            )
            count += 1
            print(f"{count=}")
        if count >= limit:
            break

    return df


def retrieve_top_posts(subreddit_name, limit=1):
    # Fetch the subreddit
    subreddit = reddit.subreddit(subreddit_name)

    # Retrieve the top 10 hot posts
    hot_posts = subreddit.top(time_filter='year', limit=limit)

    return hot_posts


# Create a DF
main_df = pd.DataFrame(columns=['subreddit', 'post_title', 'post_upvotes', 'post_link', 'comment', 'comment_upvotes'])


# Scrape comments and update the DataFrame

def main_loop(subreddit, df):
    top_posts = retrieve_top_posts(subreddit, limit=3)
    count = 0

    for p in top_posts:
        print(p.title, p.url, p.id)
        df = scrape_comments(subreddit, p.id, df, limit=10)
        count += 1
        print(f"--- DONE {count} ---")

    return df  # Return the final DataFrame

main_df = main_loop('skincareaddiction', main_df)
print(main_df)

main_df.to_csv('test_comments.csv')