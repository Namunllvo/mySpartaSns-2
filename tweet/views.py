from django.shortcuts import render, redirect
from .models import TweetModel
from .models import TweetComment
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
        user = request.user.is_authenticated        # 사용자가 지금 로그인 되어 있냐

        if user:        # 사용자가 있으면
            all_tweet = TweetModel.objects.all().order_by('-created_at')     #tweet이 생성된 시간을 역순으로 출력해주는 order_by(역순으로 정렬할수 있게 - 붙임)
            return render(request, 'tweet/home.html', {'tweet':all_tweet})      #딕셔너리 형태로 키값은 tweet, 이 데이터를 화면에 넘긴다=> 저장한 게시물을 읽어와서 tweet/home.html로 전달
        else:
            return redirect('/sign-in')
    elif request.method == 'POST':
        user = request.user
        my_tweet = TweetModel()
        my_tweet.author = user
        my_tweet.content = request.POST.get('my-content', '')
        my_tweet.save()
        return redirect('/tweet')


@login_required     # delete 함수는 로그인이 되어 있어야만 사용할 수 있는 함수
def delete_tweet(request,id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': tweet_comment})



@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/' + str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/' + str(current_tweet))

