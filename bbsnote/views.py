# django.shortcuts 모듈에서 render, redirect, get_object_or_404 함수를 가져옴
from django.shortcuts import render, redirect, get_object_or_404
# django.http 모듈에서 HttpResponse 클래스를 가져옴, HTTP 응답
from django.http import HttpResponse
# 현재 디렉토리의 models 모듈에서 Board, Comment 클래스를 가져옴, 데이터베이스 테이블
from .models import Board, Comment
# django.utils 모듈에서 timezone 모듈을 가져옴
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# 첫번째 뷰 함수 index를 정의, HTTP 요청 객체인 request를 인자로 받음
def index(request):
    # 입력인자
    page = request.GET.get('page', 1)

    # 조회
    # 데이터베이스에서 Board 객체 목록을 가져옴, 이 목록은 생성 날짜의 역순으로 정렬
    board_list = Board.objects.order_by('-create_date')
    
    # 페이징 처리
    # board_list는 페이지로 나눌 데이터 목록, 5는 한 페이지에 표시할 항목 수
    paginator = Paginator(board_list, 5)
    # get_page 메소드는 페이지 번호를 받아 해당 페이지를 리턴
    page_obj = paginator.get_page(page)
    
    # 컨텍스트 변수
    # 템플릿에 전달되어 렌더링에 사용
    context = {'board_list': page_obj}
    ## return HttpResponse("bbsnote에 오신 것을 환영합니다");
    # 템플릿 파일 'bbsnote/voard_list.html'을 렌더링하여 HTTP 응답 객체 반환
    return render(request, 'bbsnote/board_list.html', context)

# HTTP 요청 객체인 request와 정수형 변수인 board_id를 인자로 받음
def detail(request, board_id):
    # 데이터베이스에서 id가 board_id인 Board 객체를 가져옴
    board = Board.objects.get(id=board_id)
    # 컨텍스트 변수, 이 변수는 템플릿에 전달되어 렌더링에 사용
    context = {'board': board}
    # 템플릿 파일 'bbsnote/board_detail.html'을 렌더링하여 HTTP 응답 객체 반환
    return render(request, 'bbsnote/board_detail.html', context)

# 사용자가 로그인하지 않은 상태에서 이 뷰 함수에 접근하려고 할 때 common:login으로 지정된 URL로 리다이렉트
@login_required(login_url='common:login')
# 뷰 함수인 comment_create 정의
# HTTP 요청 객체인 request와 정수형 변수인 board_id를 인자로 받음
def comment_create(request, board_id):
    # POST인 경우에만 다음 코드를 실행
    if request.method == 'POST':
        # 데이터베이스에서 id가 board_id인 Board 객체를 가져옴
        board = Board.objects.get(id=board_id)

        # 이 객체의 속성값은 인자로 전달된 값으로 설정
        # 여기서 content 속성값은 POST 데이터 중 content 키의 값으로 설정
        ## comment = Comment(board=board, content=request.POST.get('content'), create_date=timezone.now())
        # Comment 객체를 데이터베이스에 저장
        ## comment.save()

        # author=request.user는 현재 로그인한 사용자의 인스턴스를 가져와서 author 필드에 설정하는 것을 의미
        board.comment_set.create(content=request.POST.get('content'), create_date=timezone.now(), author=request.user)
    # 'bbsnote:detail'로 지정된 URL로 리다이렉트, 인자로 board.id 전달
    return redirect('bbsnote:detail', board_id=board.id)

# 로그인이 되어 있지 않으면 'common:login' URL로 리다이렉션
@login_required(login_url='common:login')
# board_create라는 이름의 뷰 함수 정의, request 객체를 인자로 받음
def board_create(request):
    # 요청의 HTTP 메소드가 'POST'인지 확인
    if request.method == 'POST':
        # 'POST' 요청의 데이터를 사용하여 BoardForm 객체 생성
        form = BoardForm(request.POST)
        # valid로 True, False 폼이 유효한지 검사
        if form.is_valid():
            # 폼 데이터를 사용하여 board 객체를 생성, 데이터베이스에 저장하지 않음
            board = form.save(commit=False)
            # board 객체의 create_date 속성을 현재 시간으로 설정
            board.create_date = timezone.now()
            board.author = request.user
            # board 객체를 데이터베이스에 저장
            board.save()
            # 'bbsnote:index'라는 이름의 URL로 리다이렉트
            return redirect('bbsnote:index')
    # HTTP 메소드가 'POST'가 아닌 경우 실행
    else:
        # 빈 BoardForm 객체 생성
        form = BoardForm()
    # 'bbsnote/board_form.html' 템플릿을 사용하여 응답을 생성
    # 템플릿 컨텍스트에 'form' 변수로 폼 객체를 전달
    return render(request, 'bbsnote/board_form.html', {'form':form})

# 로그인이 되어 있지 않으면 'common:login' URL로 리다이렉션
@login_required(login_url='common:login')
# board_modify라는 함수 정의, request와 board_id 두 개의 인수를 받음
def board_modify(request, board_id):
    # Board 모델에서 pk가 board_id인 객체를 가져오고 해당 객체가 없으면 404 에러 페이지 표시
    board = get_object_or_404(Board, pk=board_id)
    # 만약 요청이 게시물의 작성자가 아니면 다음 코드 실행
    if request.user != board.author:
        # 에러메시지
        messages.error(request, '수정 권한이 없습니다')
        # 'bbsnote:detail' URL로 리다이렉션
        return redirect('bbsnote:detail', board_id=board.id)
    # 만약 요청이 'POST'면 다음 코드 실행
    if request.method == 'POST':
        # BoardForm이라는 폼 클래스의 인스턴스를 생성하고 request.POST와 board 객체를 사용하여 초기화
        form = BoardForm(request.POST, instance=board)
        # 만약 폼이 유효하면 다음 코드 실행
        if form.is_valid():
            # 폼 데이터로 board 객체를 업데이트
            # commit=False로 하여 데이터베이스에 변경 사항을 저장하지 않도록 함
            board = form.save(commit=False)
            # board 객체의 author 속성을 요청을 보낸 사용자로 설정
            board.author = request.user
            # 변경 사항을 데이터베이스에 저장
            board.save()
            # 'bbsnote:detail' URL로 리다이렉션됨, board_id라는 인수 필요
            return redirect('bbsnote:detail', board_id=board.id)
    else:
        # BoardForm이라는 폼 클래스의 인스턴스 생성
        form = BoardForm(instance=board)
    # 템플릿에서 사용할 수 있는 데이터를 포함하는 딕셔너리
    context = {'form':form}
    # 'bbsnote/board_form.html' 템플릿을 렌더링하고 HTTP 응답 반환, 컨텍스트 변수를 사용하여 렌더링
    return render(request, 'bbsnote/board_form.html', context)

# 로그인이 되어있지 않으면 'common:login' URL로 리다이렉션
@login_required(login_url='common:login')
# board_delete라는 함수 정의, request와 board_id 인수를 받음
def board_delete(request, board_id):
    # 객체가 없으면 404 에러페이지 표시
    board = get_object_or_404(Board, pk=board_id)
    # 요청을 보낸 사용자가 게시물 작성자가 아니면 다음 코드 블록이 실행됨
    if request.user != board.author:
        # 에러메시지
        messages.error(request, '삭제 권한이 없습니다')
        # 'bbsnote:detail'로 리다이렉션
        return redirect('bbsnote:detail', board_id=board.id)
    # 데이터베이스에서 삭제
    board.delete()
    # bbsnote:index'로 리다이렉션
    return redirect('bbsnote:index')

# 로그인이 되어있지 않으면 'common:login' URL로 리다이렉션
@login_required(login_url='common:login')
# comment_modify라는 함수 정의, request와 board_id를 인수로 받음
def comment_modify(request, comment_id):
    # 해당 객체가 없으면 404 에러 페이지 표시
    comment = get_object_or_404(Comment, pk=comment_id)
    # 만약 요청의 사용자가 댓글의 작성자가 아니면 다음 코드 실행
    if request.user != comment.author:
        # 에러 메시지
        messages.error(request, "수정 권한이 없습니다!")
        # 'bbsnote:detail' URL로 리다이렉션
        return redirect('bbsnote:detail', comment_id=comment.board.id)
    # 만약 요청이 'POST'이면 다음 코드 실행
    if request.method == "POST":
        # CommentForm이라는 폼 인스턴스 생성, request.POST와 comment 객체로 초기화
        form = CommentForm(request.POST, instance=comment)
        # 만약 폼이 유효하면 다음 코드 실행
        if form.is_valid():
            # 폼 데이터를 사용하여 comment 객체를 업데이트, 데이터베이스에 변경 사항을 저장하지 않음
            comment = form.save(commit=False)
            # comment 객체의 author 속성을 요청을 보낸 사용자로 설정
            comment.author = request.user
            # 변경 사항을 데이터베이스에 저장
            comment.save()
            # 'bbsnote:detail' URL로 리다이렉션
            return redirect('bbsnote:detail', board_id=comment.board.id)
    else:
        # CommentForm이라는 폼 클래스의 인스턴스 생성
        form = CommentForm(instance=comment)
    # 템플릿에서 사용할 수 있는 데이터를 포함하는 딕셔너리
    context = {'comment':comment, 'form':form}
    # 'bbsnote/comment_form.html' 템플릿을 렌더링하고 HTTP 응답 반환
    # 컨텍스트 변수를 사용하여 렌더링
    return render(request, 'bbsnote/comment_form.html', context)

# 로그인이 되어있지 않으면 'common:login' URL로 리다이렉션
@login_required(login_url='common:login')
# comment_delete라는 함수 정의, request와 comment_id를 인수로 받음
def comment_delete(request, comment_id):
    # 해당 객체가 없으면 404 에러 페이지 표시
    comment = get_object_or_404(Comment, pk=comment_id)
    # 만약 요청의 사용자가 댓글의 작성자가 아니면 다음 코드 실행
    if request.user != comment.author:
        # 에러메시지
        messages.error(request, "삭제 권한이 없습니다")
        # 'bbsnote:detail' URL로 리다이렉션
        return redirect('bbsnote:detail', board_id=comment.board.id)
    # 객체를 데이터베이스에서 삭제
    comment.delete()
    # 'bbsnote:detail' URL로 리다이렉션
    return redirect('bbsnote:detail', board_id=comment.board.id)
