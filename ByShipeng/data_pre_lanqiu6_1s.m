
clear all
data  = load('216_shipeng_lanqiu2.txt');
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
% % 
% sld_len = 5;
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

%216_shipeng2
act_kind_st = [3650 19700 34000 49240 60800 92500 121200];
act_kind_ed = [17650 32000 47100 58000 89200 120400 149000];
act_kind_value = [0 0 -0 -0 2500 -1000];
delay1 = 50 ;
delay2 = 20;

%216_changsheng_lanqiu1
% act_kind_st = [2900 18800 34300 57700 75000 108700 143500];
% act_kind_ed = [16800 31800 47700 70500 106400 140500 166500];
% act_kind_value = [0 0 -0 -0 4000 700];

% act_value = [];
step1 = 50;
step2 = 100;
dd(1,1) = 1;
sensor = [ax ay az gx gy gz];
j = 0;
   for i = act_kind_st(1):step1:act_kind_ed(1)
             j = j + 1;
            feature(j,:) =[1 feature_extraction6_1s(sensor(i : i + step2-1,:),j)];
            dd(j,1) = i;
            if j == 50
                break;
            end
   end
   j
   for i = act_kind_st(2):step1:act_kind_ed(2)
             j = j + 1;
           feature(j,:) =[2 feature_extraction6_1s(sensor(i : i + step2-1,:))];
            dd(j,1) = i;
            if j == 100
                break;
            end
   end
   j
    for i = act_kind_st(5):act_kind_ed(5)
        if aax( i ) > act_kind_value(5) && i - dd(j) > 6*step1 
             j = j + 1;
            feature(j,:) =[3 feature_extraction6_1s(sensor(i + delay1 : i + delay1 + step2-1,:))];
            dd(j,1) = i + delay1;
        end
    end
    j
   for i = act_kind_st(3):step1:act_kind_ed(3)
            j = j + 1;
            feature(j,:) =[4 feature_extraction6_1s(sensor(i : i + step2-1,:))];
            dd(j,1) = i;
            if j == 200
                break;
            end
   end
   for i = act_kind_st(4):step1:act_kind_ed(4)
            j = j + 1;
           feature(j,:) =[5 feature_extraction6_1s(sensor(i : i + step2-1,:))];
            dd(j,1) = i;
            if j  == 250
                break;
            end
   end
   j
   
   for i = act_kind_st(6):act_kind_ed(6)
        if aax( i )< act_kind_value(6) && i - dd(j) > 5*step1 
            j = j + 1;
            feature(j,:) =[6 feature_extraction6_1s(sensor(i + delay2 : i + delay2 +step2-1,:))];
            dd(j,1) = i + delay2;
        end
   end
   j


% fid = fopen('216_shipeng_lanqiu2_feature','wt');
% fprintf(fid,'%d 1:%f 2:%f 3:%f 4:%f 5:%f 6:%f 7:%f 8:%f 9:%f 10:%f 11:%f 12:%f 13:%f 14:%f 15:%f 16:%f 17:%f 18:%f 19:%f 20:%f 21:%f 22:%f 23:%f 24:%f 25:%f 26:%f 27:%f 28:%f 29:%f 30:%f 31:%f 32:%f 33:%f 34:%f 35:%f 36:%f 37:%f 38:%f 39:%f 40:%f 41:%f 42:%f 43:%f 44:%f 45:%f 46:%f 47:%f 48:%f 49:%f 50:%f 51:%f\r\n',feature');
% fclose(fid);
fid = fopen('216_shipeng_lanqiu2_feature6_1s_abs.txt','wt');
[a b] = size(feature);
for i = 1 : a
    fprintf(fid,'%d ',feature(i,1));
    for k = 2:b
        fprintf(fid,'%f ',feature(i,k));
    end
        fprintf(fid,'\r\n');    
end
fclose(fid);


jj = 1;
   for i = act_kind_st(7):step1:act_kind_ed(7)
            feature_test(jj,:) =[-1 feature_extraction6_1s(sensor(i : i + step2-1,:))];
            jj = jj +1;
            j = j + 1;
           dd(j,1) = i;
   end
fid = fopen('216_shipeng_lanqiu2_featuretest6_1s_abs.txt','wt');
[a b] = size(feature_test);
for i = 1 : a
    fprintf(fid,'%d ',feature_test(i,1));
    for k = 2:b
        fprintf(fid,'%f ',feature_test(i,k));
    end
        fprintf(fid,'\r\n');    
end
fclose(fid);

aa = [1:step1:len];
bb = zeros(length(aa),1);
% dd = [1:step1*10:len];
ee = zeros(length(dd),1);
figure name 'window'
axis equal
plot(1:len,data(:,1),'b',aa,bb,'*r',dd,ee,'ok')
















