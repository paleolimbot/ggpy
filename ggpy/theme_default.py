from ggpy._grob.unit import Unit
from ._na import NA
from .margins import Margin
from .theme import Theme
from .theme_elements import element_blank, element_line, element_rect, element_text, Rel


def theme_grey(base_size=11, base_family='Arial'):
    half_line=base_size / 2

    # Elements in this first block aren't used directly, but are inherited
    # by others
    return Theme(complete=True,
                 line=element_line(colour="black", size=0.5, linetype=1, lineend="butt"),
                 rect=element_rect(fill="white", colour="black", size=0.5, linetype=1),
                 text=element_text(family=base_family, face="plain", colour="black", size=base_size,
                                   lineheight=0.9, hjust=0.5, vjust=0.5, angle=0, margin=Margin()),
                 axis_line=element_line(),
                 axis_line_x=element_blank(),
                 axis_line_y=element_blank(),
                 axis_text=element_text(size=Rel(0.8), colour="grey30"),
                 axis_text_x=element_text(margin=Margin(t=0.8 * half_line / 2), vjust=1),
                 axis_text_y=element_text(margin=Margin(r=0.8 * half_line / 2), hjust=1),
                 axis_ticks=element_line(colour="grey20"),
                 axis_ticks_length= Unit(half_line / 2, "pt"),
                 axis_title_x=element_text(margin=Margin(t=0.8 * half_line, b=0.8 * half_line / 2)),
                 axis_title_y=element_text(angle=90, margin=Margin(r=0.8 * half_line, l=0.8 * half_line / 2)),
                 legend_background=element_rect(colour=NA),
                 legend_margin=Unit(0.2, "cm"),
                 legend_key=element_rect(fill="grey95", colour="white"),
                 legend_key_size=Unit(1.2, "lines"),
                 legend_key_height=NA,
                 legend_key_width=NA,
                 legend_text=element_text(size=Rel(0.8)),
                 legend_text_align=NA,
                 legend_title=element_text(hjust=0),
                 legend_title_align=NA,
                 legend_position="right",
                 legend_direction=NA,
                 legend_justification="center",
                 legend_box=NA,
                 panel_background=element_rect(fill="grey92", colour=NA),
                 panel_border=element_blank(),
                 panel_grid_major=element_line(colour="white"),
                 panel_grid_minor=element_line(colour="white", size=0.25),
                 panel_margin=Unit(half_line, "pt"),
                 panel_margin_x=NA,
                 panel_margin_y=NA,
                 panel_ontop=False,
                 strip_background=element_rect(fill="grey85", colour=NA),
                 strip_text=element_text(colour="grey10", size=Rel(0.8)),
                 strip_text_x=element_text(margin=Margin(t=half_line, b=half_line)),
                 strip_text_y=element_text(angle=-90, margin=Margin(l=half_line, r=half_line)),
                 strip_switch_pad_grid=Unit(0.1, "cm"),
                 strip_switch_pad_wrap=Unit(0.1, "cm"),
                 plot_background=element_rect(colour="white"),
                 plot_title=element_text(size=Rel(1.2), hjust=0, margin=Margin(b=half_line * 1.2)),
                 plot_subtitle=element_text(size=Rel(0.9), hjust=0, margin=Margin(b=half_line * 0.9)),
                 plot_caption=element_text(size=Rel(0.9), hjust=1, margin=Margin(t=half_line * 0.9)),
                 plot_margin=Margin(half_line, half_line, half_line, half_line))
