extends Control

func _process(delta):
	if Input.is_key_pressed(KEY_R):
		get_tree().change_scene_to_file("res://main.tscn")
