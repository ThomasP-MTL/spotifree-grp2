FROM archlinux


ENV user=jenkins

RUN pacman -Sy --noconfirm
RUN pacman -S openssh --noconfirm
RUN pacman -S jdk8-openjdk git maven--noconfirm

RUN useradd -m $user
RUN mkdir /home/jenkins/.ssh && chown jenkins: -R /home/jenkins


RUN ssh-keygen -A

COPY jenkins_rsa.pub /home/jenkins/.ssh/authorized_keys

EXPOSE 2223

CMD ["/usr/sbin/sshd","-D"]




