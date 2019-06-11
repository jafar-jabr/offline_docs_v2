
class AppDimension:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def get_dim(self, dim):
        dimensions = {
            'main_table_w': self.w-10,
            'all_visits_table_w': self.w-10,
            'main_inner_w': min(1000, self.w-10),
            'staff_table_w': int(self.w*0.78),
            'login_width': 500,
            'login_height': 370,
            'main_window_height': self.h,
            'main_window_width': self.w,
            'default_font_size': 18
        }
        return dimensions[dim]