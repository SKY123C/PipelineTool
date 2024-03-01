from rvcore.base_classes import base_command
import cgtw2


class OpenTW(base_command.RVCommand):
    long_name = "open"
    shot_name = "o"
    
    @staticmethod
    def run(args):
        tw = cgtw2.tw()
        ip = tw.login.http_server_ip()
        tw.send_local_socket("main_widget", "activate_window", {}, "send")
        db = args.db
        token = tw.login.token()
        module = args.module
        module_type = args.mt
        task_id = args.taskId
        lang=tw.send_local_socket("main_widget", "get_client_language", {}, "get")
        theme=tw.send_local_socket("main_widget", "get_client_theme", {}, "get")
        t_url="https://"+ip+"/index.php?controller=v_main_window&method=show_page&db="+db+"&code="+db+"&module="+module+"&module_type="+module_type+"&is_qt=y&token="+token+"&lang="+lang+"&theme="+theme
        t_dic={"url":t_url, "key":db, "text":"Big", "cookie_data":task_id}
        tw.send_local_socket("main_widget", "create_project_widget", t_dic, "send")

    
        
        
        
        