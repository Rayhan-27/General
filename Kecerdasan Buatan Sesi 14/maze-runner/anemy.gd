extends CharacterBody2D

enum State {PATROL, CHASE, ATTACK}

var state = State.PATROL
var patrol_target = Vector2(400, 300)
var speed = 100
var detect_range = 200
var attack_range = 50
var patrol_timer = 0

@onready var player = get_parent().get_node("Player")

func _physics_process(delta):
	patrol_timer += delta
	var distance = global_position.distance_to(player.global_position)
	
	# FSM - cek state
	if distance < attack_range:
		state = State.ATTACK
	elif distance < detect_range:
		state = State.CHASE
	else:
		state = State.PATROL
	
	# Jalankan aksi sesuai state
	match state:
		State.PATROL:
			do_patrol(delta)
		State.CHASE:
			do_chase()
		State.ATTACK:
			do_attack()
	
	move_and_slide()
	
	# Tampilkan state di title window
	# Tampilkan state di HUD
	var label = get_parent().get_node("CanvasLayer/HUD")
	if label:
		match state:
			State.PATROL:
				label.text = "Enemy State: PATROL"
			State.CHASE:
				label.text = "Enemy State: CHASE"
			State.ATTACK:
				label.text = "Enemy State: ATTACK"

func do_patrol(delta):
	if patrol_timer > 3.0 or global_position.distance_to(patrol_target) < 10:
		patrol_timer = 0
		patrol_target = Vector2(randi_range(50, 750), randi_range(50, 550))
	var dir = (patrol_target - global_position).normalized()
	velocity = dir * (speed * 0.5)

func do_chase():
	var dir = (player.global_position - global_position).normalized()
	velocity = dir * speed

func do_attack():
	velocity = Vector2.ZERO
	get_tree().change_scene_to_file("res://game_over.tscn")
