from django.shortcuts import get_object_or_404
from django.urls import resolve
from HomeModule.models import UserActivity



class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
    
    
class ActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Track visits on a page
        if request.user.is_authenticated:
            # Get the resolved view name and check if it matches any of your tracked pages
            resolved_view_name = resolve(request.path_info).view_name
            print(resolved_view_name)
            tracked_pages = ['home', 'blog-post', 'profile']
            if resolved_view_name in tracked_pages:
                # Create a new UserActivity instance and save it to the database
                activity = UserActivity(
                    user=request.user,
                    activity_type='page_visit',
                    activity_details=resolved_view_name
                )
                print("jbdsfkdjsb")
                activity.save()
    
    # def process_response(self, request, response):
    #     # Track likes on a post
    #     if request.user.is_authenticated:
    #         if request.path.startswith('/post/'):
    #             # Get the post object and check if the user has liked it
    #             post_id = request.path.split('/')[-2]
    #             post = get_object_or_404(Post, id=post_id)
    #             if request.user in post.likes.all():
    #                 # Create a new UserActivity instance and save it to the database
    #                 activity = UserActivity(
    #                     user=request.user,
    #                     activity_type='post_like',
    #                     activity_details=post_id
    #                 )
    #                 activity.save()
        
    #     return response


