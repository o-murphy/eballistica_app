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

# set_unit_velocity = Signal(args=['unit'], name='set_v_unit')  # TODO: Deprecated
# set_unit_distance = Signal(args=['unit'], name='set_dt_unit')  # TODO: Deprecated
# set_unit_temperature = Signal(args=['unit'], name='set_t_unit')  # TODO: Deprecated
# set_unit_weight = Signal(args=['unit'], name='set_w_unit')  # TODO: Deprecated
#
# set_unit_length = Signal(args=['unit'], name='set_ln_unit')  # TODO: Deprecated
# set_unit_diameter = Signal(args=['unit'], name='set_dm_unit')  # TODO: Deprecated
# set_unit_pressure = Signal(args=['unit'], name='set_ps_unit')  # TODO: Deprecated
# set_unit_drop = Signal(args=['unit'], name='set_dp_unit')  # TODO: Deprecated
# set_unit_angular = Signal(args=['unit'], name='set_an_unit')  # TODO: Deprecated
# set_unit_adjustment = Signal(args=['unit'], name='set_unit_adjustment')  # TODO: Deprecated
# set_unit_energy = Signal(args=['unit'], name='set_e_unit')  # TODO: Deprecated

set_theme = Signal(args=['theme'], name='set_theme')
set_lang = Signal(args=['lang'], name='set_lang')

load_set_theme = Signal(args=['theme'], name='load_set_theme')
load_set_lang = Signal(args=['lang'], name='load_set_theme')

load_unit_sight_height = Signal(args=['unit'], name='load_set_sh_unit')
load_unit_twist = Signal(args=['unit'], name='load_set_tw_unit')
load_unit_velocity = Signal(args=['unit'], name='load_set_v_unit')
load_unit_distance = Signal(args=['unit'], name='load_set_dt_unit')
load_unit_temperature = Signal(args=['unit'], name='load_set_t_unit')
load_unit_weight = Signal(args=['unit'], name='load_set_w_unit')

load_unit_length = Signal(args=['unit'], name='load_set_ln_unit')
load_unit_diameter = Signal(args=['unit'], name='load_set_dm_unit')
load_unit_pressure = Signal(args=['unit'], name='load_set_ps_unit')
load_unit_drop = Signal(args=['unit'], name='load_set_dp_unit')
load_unit_angular = Signal(args=['unit'], name='load_set_an_unit')
load_unit_adjustment = Signal(args=['unit'], name='load_set_unit_adjustment')
load_unit_energy = Signal(args=['unit'], name='load_set_e_unit')

set_settings = Signal(args=['target', 'value'], name='set_settings')
load_setting = Signal(name='load_setting')
