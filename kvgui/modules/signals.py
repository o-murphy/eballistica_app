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
