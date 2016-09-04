clear all;
data = load('216_ganrao1.txt');
len = length(data);
aax = data(:,1);
aay = data(:,2);
aaz = data(:,3);
data(:,1:3) = data(:,1:3)/2048;
data(:,4:6) = data(:,4:6)/32.8;

ax = data(:,1);
ay = data(:,2);
az = data(:,3);
gx = data(:,4);
gy = data(:,5);
gz = data(:,6);

% sld_len = 10;
% for i = 1+sld_len: length(data)-sld_len
%     ax(i) = mean(data(i - sld_len+1 : i + sld_len,1));
%     ay(i) = mean(data(i - sld_len+1 : i + sld_len,2));
%     az(i) = mean(data(i - sld_len+1 : i + sld_len,3));
%     gx(i) = mean(data(i - sld_len+1 : i + sld_len,1));
%     gy(i) = mean(data(i - sld_len+1 : i + sld_len,2));
%     gz(i) = mean(data(i - sld_len+1 : i + sld_len,3));
% end
% 
% for  i = 1:sld_len
%     ax(i) = data(i,1); 
%     ax(length(data)-i+1) = data(length(data)-i+1,1);
%     ay(i) = data(i,2); 
%     ay(length(data)-i+1) = data(length(data)-i+1,2);
%     az(i) = data(i,3); 
%     az(length(data)-i+1) = data(length(data)-i+1,3);
%     gx(i) = data(i,4); 
%     gx(length(data)-i+1) = data(length(data)-i+1,4);
%     gy(i) = data(i,5); 
%     gy(length(data)-i+1) = data(length(data)-i+1,5);
%     gz(i) = data(i,6); 
%     gz(length(data)-i+1) = data(length(data)-i+1,6);
%     
% end
% ax = ax';
% ay = ay';
% az = az';
% gx = gx';
% gy = gy';
% gz = gz';

step1 = 50;
step2 = 100;
j = 1;
sensor = [ax ay az gx gy gz];
dd = [];
for i = 1:step1:length(data)-step2
    feature(j,:) =[0 feature_extraction6_1s(sensor(i : i + step2-1,:))];
    dd = [dd; i 0];
    j = j +1;
end
figure 
plot(1:length(ax),ax,'b',dd(:,1), dd(:,2),'ro');

% fid = fopen('216_shipeng_lanqiu_test2_feature6.txt','wt');
% fprintf(fid,'%d %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\r\n',feature');
% fclose(fid);

% fid = fopen('216_ganrao1_feature7.txt','wt');
% fprintf(fid,'%d %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\r\n',feature');
% fclose(fid);


% fid = fopen('216_ganrao1_feature7.txt','wt');
% fprintf(fid,'%d %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\r\n',feature');
% fclose(fid);


% fid = fopen('216_shipeng_lanqiu_test2_feature8.txt','wt');
% fprintf(fid,'%d %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f  %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\r\n',feature');
% fclose(fid);

fid = fopen('216_ganrao1_feature6_1s.txt','wt');
[a b] = size(feature);
for i = 1 : a
    fprintf(fid,'%d ',feature(i,1));
    for j = 2:b
        fprintf(fid,'%f ',feature(i,j));
    end
        fprintf(fid,'\r\n');    
end
fclose(fid);










