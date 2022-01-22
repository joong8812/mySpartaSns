from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다.', 'tweet':all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            my_tweet.save()
            return redirect('/tweet')


def detail_tweet(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            this_tweet = TweetModel.objects.get(id=id)
            all_comments = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
            return render(request, 'tweet/tweet_detail.html', {'tweet': this_tweet, 'comment': all_comments})
        else:
            return redirect('/sign-in')


def write_comment(request, id):
    if request.method == 'POST':
        user = request.user.is_authenticated
        if user:
            tweet = TweetModel.objects.get(id=id)
            my_comment = TweetComment()
            my_comment.author = request.user
            my_comment.tweet = tweet
            my_comment.comment = request.POST.get('comment', '')
            my_comment.save()
            return redirect(f'/tweet/{id}')
        else:
            return redirect('/sign-in')


@login_required
def delete_comment(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            my_comment = TweetComment.objects.get(id=id)
            tweet_id = my_comment.tweet.id
            my_comment.delete()
            return redirect(f'/tweet/{tweet_id}')
        else:
            return redirect('/sign-in')


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')