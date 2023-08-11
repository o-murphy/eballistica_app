from signalslot import Signal


top_bar_cog_act = Signal(name='settings_cicked')
top_bar_apply_act = Signal(name='settings_cicked')

bot_bar_back_act = Signal(name='back_act_clicked')
bot_bar_fab_act = Signal(args=['caller'], name='fab_clicked')

rifle_item_touch = Signal(args=['caller'], name='rifle_item_touch')
rifle_item_long_touch = Signal(args=['caller'], name='rifle_item_long_touch')
rifle_edit_act = Signal(args=['caller'], name='rifle_edit_act')
rifle_del_act = Signal(args=['caller'], name='rifle_edit_act')

ammo_item_touch = Signal(args=['caller'], name='ammo_item_touch')
ammo_item_long_touch = Signal(args=['caller'], name='ammo_item_long_touch')
ammo_edit_act = Signal(args=['caller'], name='ammo_edit_act')
ammo_del_act = Signal(args=['caller'], name='ammo_edit_act')

ammo_dm_change = Signal(args=['caller'], name='ammo_dm_change')
ammo_powder_sens_act = Signal(args=['caller'], name='ammo_powder_sens_act')

one_shot_act = Signal(args=['caller'], name='one_shot_act')
trajectory_act = Signal(args=['caller'], name='trajectory_act')

set_sh_unit_change = Signal(args=['unit'], name='set_sh_unit')
set_tw_unit_change = Signal(args=['unit'], name='set_tw_unit')
set_v_unit_change = Signal(args=['unit'], name='set_v_unit')
set_dt_unit_change = Signal(args=['unit'], name='set_dt_unit')
set_t_unit_change = Signal(args=['unit'], name='set_t_unit')
set_w_unit_change = Signal(args=['unit'], name='set_w_unit')
set_ln_unit_change = Signal(args=['unit'], name='set_ln_unit')
set_dm_unit_change = Signal(args=['unit'], name='set_dm_unit')
set_ps_unit_change = Signal(args=['unit'], name='set_ps_unit')
set_dp_unit_change = Signal(args=['unit'], name='set_dp_unit')
set_an_unit_change = Signal(args=['unit'], name='set_an_unit')
set_ad_unit_change = Signal(args=['unit'], name='set_ad_unit')
set_e_unit_change = Signal(args=['unit'], name='set_e_unit')
