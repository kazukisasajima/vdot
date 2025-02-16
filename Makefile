# Docker Compose の設定
COMPOSE=docker-compose
DOCKER_DIR=./docker

# 引数でコンテナ名を受け取る（デフォルトは全てのサービス）
SERVICE=$(filter-out $@,$(MAKECMDGOALS))

# Docker コンテナのビルド（サービス指定可能）
build:
	cd $(DOCKER_DIR) && $(COMPOSE) build $(SERVICE)

# コンテナの起動（サービス指定可能）
up:
	cd $(DOCKER_DIR) && $(COMPOSE) up -d $(SERVICE)

# コンテナの停止（サービス指定可能）
stop:
	cd $(DOCKER_DIR) && $(COMPOSE) stop $(SERVICE)

# コンテナの再起動（サービス指定可能）
restart:
	cd $(DOCKER_DIR) && $(COMPOSE) restart $(SERVICE)

# コンテナの削除（サービス指定可能）
down:
	cd $(DOCKER_DIR) && $(COMPOSE) stop $(SERVICE) && $(COMPOSE) rm -f $(SERVICE)

# コンテナのログを表示（サービス指定可能）
logs:
	cd $(DOCKER_DIR) && $(COMPOSE) logs -f $(SERVICE)

# 起動中のコンテナの状態を確認
ps:
	cd $(DOCKER_DIR) && $(COMPOSE) ps

# 不要なコンテナ・イメージ・ボリュームを削除（完全削除）
clean:
	cd $(DOCKER_DIR) && $(COMPOSE) down --volumes --rmi all

# Makefileのターゲットとして認識しないようにする
%:
	@:
