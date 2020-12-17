filename= '/result2.csv';
data=csvread(filename);
x=data(:,3);
y1=data(:,4);
y2=data(:,5);


% figure(1)
% p1=data(:,4);
% p2=data(:,5);
% plot(p1,p2,'b.')
% xlabel('exact priority')
% ylabel('estimated priority')

figure(1)
x3=1:36420;
plot(x3,y1,'r+')
hold on
plot(x3,y2,'b.')
ylabel('priority')
legend('exact','estimator')

figure(2)
dif=y1-y2;
plot(x3,dif,'b*')
ylabel('exact-estimated')

absdif=abs(y1-y2);
sum0=sum(absdif(:)==0)
ratio0=sum0/36420
sum1=sum(absdif(:)==1)
ratio1=sum1/36420
sum2=sum(absdif(:)==2)
ratio2=sum2/36420
sum3=sum(absdif(:)==3)
ratio3=sum3/36420
sum4=sum(absdif(:)==4)
ratio4=sum4/36420
rmse=sqrt((1*sum1+4*sum2+9*sum3+16*sum4)/36420)
mae=(sum1+2*sum2+3*sum3+4*sum4)/36420

y1y2=[y1,y2];
p1=[];
hitp1=0;
for i= 1:36420
    if y1y2(i,1)==1
      p1=[p1 y1y2(i,2)];
      if y1y2(i,2)==1
          hitp1=hitp1+1;
      end
    end
end
figure(3)
p1x=1:129;
plot(p1x,p1,'r*')
ylabel('priority')
title('the bugs we suppose to be p1 really are p?')
hitp1=hitp1/129

y1y2=[y1,y2];
p3=[];
hitp3=0;
for i= 1:36420
    if y1y2(i,1)==3
      p3=[p3 y1y2(i,2)];
      if y1y2(i,2)==3
          hitp3=hitp3+1;
      end
    end
end
figure(4)
p3x=1:32567;
plot(p3x,p3,'r*')
title('the bugs we suppose to be p3 really are p?')
ylabel('priority')
hitp3=hitp3/32567

p5=[];
hitp5=0;
for i= 1:36420
    if y1y2(i,1)==5
      p5=[p5 y1y2(i,2)];
      if y1y2(i,2)==5
          hitp5=hitp5+1;
      end
    end
end
figure(5)
p5x=1:2020;
plot(p5x,p5,'r*')
title('the bugs we suppose to be p5 really are p?')
ylabel('priority')
hitp5=hitp5/2020

% y1y2=[y1,y2];
% sum11=sum(y1y2(:,1:2)==[1,1])
% sum12=sum(y1y2(:,1:2)==[1,2])
% sum13=sum(y1y2(:,1:2)==[1,3])
% sum14=sum(y1y2(:,1:2)==[1,4])
% sum15=sum(y1y2(:,1:2)==[1,5])
% sum21=sum(y1y2(:,1:2)==[2,1])
% sum22=sum(y1y2(:,1:2)==[2,2])
% sum23=sum(y1y2(:,1:2)==[2,3])
% sum24=sum(y1y2(:,1:2)==[2,4])
% sum25=sum(y1y2(:,1:2)==[2,5])
% sum31=sum(y1y2(:,1:2)==[3,1])
% sum32=sum(y1y2(:,1:2)==[3,2])
% sum33=sum(y1y2(:,1:2)==[3,3])
% sum34=sum(y1y2(:,1:2)==[3,4])
% sum35=sum(y1y2(:,1:2)==[3,5])
% sum41=sum(y1y2(:,1:2)==[4,1])
% sum42=sum(y1y2(:,1:2)==[4,2])
% sum43=sum(y1y2(:,1:2)==[4,3])
% sum44=sum(y1y2(:,1:2)==[4,4])
% sum45=sum(y1y2(:,1:2)==[4,5])
% sum51=sum(y1y2(:,1:2)==[5,1])
% sum52=sum(y1y2(:,1:2)==[5,2])
% sum53=sum(y1y2(:,1:2)==[5,3])
% sum54=sum(y1y2(:,1:2)==[5,4])
% sum55=sum(y1y2(:,1:2)==[5,5])


