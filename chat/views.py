from django.shortcuts import render

from .services import handle_intent, parse_message
from task_manager.services import daily_review, list_tasks


def _sidebar_context() -> dict:
    review = daily_review()
    return {
        'open_tasks': list_tasks(status='open'),
        'overdue_tasks': list_tasks(status='open', overdue=True),
        'completed_today': review['completed_today'],
    }


def chat(request):
    if request.method == 'GET':
        return render(request, 'chat/message.html', _sidebar_context())

    if request.method == 'POST':
        message = request.POST.get('user_message', '').strip()

        if not message:
            context = _sidebar_context() | {'error_text': 'Please enter a message.'}
            return render(request, 'chat/message.html', context)

        try:
            parsed = parse_message(message)
            result = handle_intent(parsed)

            if parsed.error is not None:
                result['error_text'] = parsed.error

        except ValueError as e:
            result = {'error_text': str(e)}
        except Exception as e:
            result = {'error_text': f'Failed to process your message: {str(e)}'}

        return render(request, 'chat/message.html', _sidebar_context() | result)
