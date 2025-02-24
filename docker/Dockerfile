# FROM python:3.9
# ENV PYTHONUNBUFFERED 1

# # 作業ディレクトリをプロジェクトルート (`vdot/`) に統一
# WORKDIR /vdot

# # 依存関係のインストール
# COPY ../requirements.txt /vdot/
# RUN pip install --upgrade pip && pip install -r /vdot/requirements.txt

# # プロジェクトの全ファイルをコピー（Docker関連も含める）
# COPY ../ /vdot/


FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /vdot
COPY ./requirements.txt /vdot/
RUN pip install --upgrade pip && pip install -r /vdot/requirements.txt
COPY . /vdot/
