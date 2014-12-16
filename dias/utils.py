from collections import OrderedDict

week_days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

def sort_days(unsortedList):
	sorted_list = []
	for day in week_days:
		for slot in unsortedList:
			if slot.week_day == day:
				sorted_list.append(slot)
	return sorted_list

def sort_slots_dict(unsortedDict):
	sorted_dict = OrderedDict()
	for day in week_days:
		for slotday,slots in unsortedDict.items():
			if slotday == day:
				sorted_dict[slotday] = slots
	return sorted_dict

def merge_slots(slots):
	merged_slots = {}
	for slot in slots:
		merged_slots[slot.week_day] = []
	ordered_slots_dict = sort_slots_dict(merged_slots)
	for slot in slots:
		slot_times = ordered_slots_dict[slot.week_day]
		slot_times_tuple = (slot.begin_time,slot.end_time)
		slot_times.append(slot_times_tuple)
	return ordered_slots_dict

def get_slot_hours(slotList):
	hours_list = []
	for one_slot in slotList:
		begin = one_slot[0].hour
		end = one_slot[1].hour
		tempList = range(begin,end)
		for tmp in tempList:
			hours_list.append(tmp)
	return hours_list