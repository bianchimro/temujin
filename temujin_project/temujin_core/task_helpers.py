from celery import Task
import websockets

class WebSocketExceptionTask(Task):
    abstract = True
    #def after_return(self, *args, **kwargs):
    #    print 'x!!!!!!!!!!!!!!!Task returned: {0!r}'.format(self.request)
    
    def on_success(self, retval, task_id, args, kwargs):
        out = {}
        out['result'] = retval
        out['state'] = 'success'
        out['token'] = task_id
        websockets.publish_result_message(out)
        

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        msg = { 
                'token' : task_id,
                'error' : { 'exception' : str(einfo.exception), 'traceback' : str(einfo.traceback)},
                'state' : 'error'
              }
        websockets.publish_result_message(msg)