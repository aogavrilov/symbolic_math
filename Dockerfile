FROM python:3.11

WORKDIR /app


RUN apt -y update && apt -y upgrade
RUN apt install -y curl git
RUN curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf |\
       bash -s -- --default-toolchain leanprover/lean4:stable -y

ENV PATH="/root/.elan/bin:$PATH"
RUN mkdir /opt/new_project
WORKDIR /opt/new_project

RUN lake +leanprover-community/mathlib4:lean-toolchain new project_name math
WORKDIR /opt/new_project/project_name
RUN lake exe cache get
RUN echo "import Mathlib.Data.Real.Basic" > ProjectName/mathlib_test.v4.lean
RUN lake lean ProjectName/mathlib_test.v4.lean
RUN ls
COPY . /opt/new_project/project_name


RUN pip install fastapi uvicorn


EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
