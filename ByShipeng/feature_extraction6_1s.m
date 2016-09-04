function feature = feature_extraction6_1s(data,varargin)
if size(varargin) ~= 0
    printflag = varargin{1};
end
 ax = data(:,1);
 ay = data(:,2);
 az = data(:,3);
 gx = data(:,4)/57.3;
 gy = data(:,5)/57.3;
 gz = data(:,6)/57.3;
 absax = abs(ax);
 absay = abs(ay);
 absaz = abs(az);
 absgx = abs(gx);
 absgy = abs(gy);
 absgz = abs(gz);
 feature = [];
 len = length(ax);
 step = 50;
 step1 = 100;
 sensor = [ax ay az gx gy gz];
 acc = sqrt(ax.^2+ay.^2+az.^2);
 gxyz = abs(gx) + abs(gy) +abs(gz);
for i = 1:step:step1
    %平均值
    meanax = mean(ax(i:i+step-1));
    meanay = mean(ay(i:i+step-1));
    meanaz = mean(az(i:i+step-1));
    meangx = mean(gx(i:i+step-1));
    meangy = mean(gy(i:i+step-1));
    meangz = mean(gz(i:i+step-1));
    meanacc = mean(acc(i:i+step-1));
    meangxyz = mean(gxyz(i:i+step-1));
    %方差
    varax = var(ax(i:i+step-1));
    varay = var(ay(i:i+step-1));
    varaz = var(az(i:i+step-1));
    vargx = var(gx(i:i+step-1));
    vargy = var(gy(i:i+step-1));
    vargz = var(gz(i:i+step-1));
    varacc = var(acc(i:i+step-1));
    vargxyz = var(gxyz(i:i+step-1));
    %标准差
    stdax = sqrt(varax);
    stday = sqrt(varay);
    stdaz = sqrt(varaz);
    stdgx = sqrt(vargx);
    stdgy = sqrt(vargy);
    stdgz = sqrt(vargz);
    stdacc = sqrt(varacc);
    stdgxyz = sqrt(vargxyz);
    %最大值
    maxax = max(ax(i:i+step-1));
    maxay = max(ay(i:i+step-1));
    maxaz = max(az(i:i+step-1));
    maxgx = max(gx(i:i+step-1));
    maxgy = max(gy(i:i+step-1));
    maxgz = max(gz(i:i+step-1));
    maxacc = max(acc(i:i+step-1));
    maxgxyz = max(gxyz(i:i+step-1));
    %最小值
    minax = min(ax(i:i+step-1));
    minay = min(ay(i:i+step-1));
    minaz = min(az(i:i+step-1));
    mingx = min(gx(i:i+step-1));
    mingy = min(gy(i:i+step-1));
    mingz = min(gz(i:i+step-1));
    mingxyz = min(gxyz(i:i+step-1));
    minacc = min(acc(i:i+step-1));
    %错位相减，对差求和
    aax = [ax(i+1:i+step-1)];
    aaax = [ax(i:i+step-2)];
    sumslpax = sum(aax-aaax)/2;
    aax = [ay(i+1:i+step-1)];
    aaax = [ay(i:i+step-2)];
    sumslpay = sum(aax-aaax)/2;
    aax = [az(i+1:i+step-1)];
    aaax = [az(i:i+step-2)];
    sumslpaz = sum(aax-aaax)/2;
    aax = [gx(i+1:i+step-1)];
    aaax = [gx(i:i+step-2)];
    sumslpgx = sum(aax-aaax)/2;
    aax = [gy(i+1:i+step-1)];
    aaax = [gy(i:i+step-2)];
    sumslpgy = sum(aax-aaax)/2;
    aax = [gz(i+1:i+step-1)];
    aaax = [gz(i:i+step-2)];
    sumslpgz = sum(aax-aaax)/2;
    aax = [acc(i+1:i+step-1)];
    aaax = [acc(i:i+step-2)];
    sumslpacc = sum(aax-aaax)/2;
    aax = [gxyz(i+1:i+step-1)];
    aaax = [gxyz(i:i+step-2)];
    sumslpgxyz = sum(aax-aaax)/2;
    %协内积和
    coraxay = sum((ax(i:i+step-1) - meanax).*(ay(i:i+step-1) - meanay))/(step -1);
    coraxaz = sum((ax(i:i+step-1) - meanax).*(az(i:i+step-1) - meanaz))/(step -1);
    coraxgx = sum((ax(i:i+step-1) - meanax).*(gx(i:i+step-1) - meangx))/(step -1);
    coraxgy = sum((ax(i:i+step-1) - meanax).*(gy(i:i+step-1) - meangy))/(step -1);
    coraxgz = sum((ax(i:i+step-1) - meanax).*(gz(i:i+step-1) - meangz))/(step -1);
    corayaz = sum((ay(i:i+step-1) - meanay).*(az(i:i+step-1) - meanaz))/(step -1);
    coraygx = sum((ay(i:i+step-1) - meanay).*(gx(i:i+step-1) - meangx))/(step -1);
    coraygy = sum((ay(i:i+step-1) - meanay).*(gy(i:i+step-1) - meangy))/(step -1);
    coraygz = sum((ay(i:i+step-1) - meanay).*(gz(i:i+step-1) - meangz))/(step -1);
    corazgx = sum((az(i:i+step-1) - meanaz).*(gx(i:i+step-1) - meangx))/(step -1);
    corazgy = sum((az(i:i+step-1) - meanaz).*(gy(i:i+step-1) - meangy))/(step -1);
    corazgz = sum((az(i:i+step-1) - meanaz).*(gz(i:i+step-1) - meangz))/(step -1);
    corgxgy = sum((gx(i:i+step-1) - meangx).*(gy(i:i+step-1) - meangy))/(step -1);
    corgxgz = sum((gx(i:i+step-1) - meangx).*(gz(i:i+step-1) - meangz))/(step -1);
    corgygz = sum((gy(i:i+step-1) - meangy).*(gz(i:i+step-1) - meangz))/(step -1);
    
    fftax = abs(fft(ax(i:i+step-1)));
    fftay = abs(fft(ay(i:i+step-1)));
    fftaz = abs(fft(az(i:i+step-1)));
    fftgx = abs(fft(gx(i:i+step-1)));
    fftgy = abs(fft(gy(i:i+step-1)));
    fftgz = abs(fft(gz(i:i+step-1)));
    
    engyax = sum(fftax.^2) /step;
    engyay = sum(fftay.^2) /step;
    engyaz = sum(fftaz.^2) /step;
    engygx = sum(fftgx.^2) /step;
    engygy = sum(fftgy.^2) /step;
    engygz = sum(fftgz.^2) /step;
    
    upax = 0;
    upay = 0;
    upaz = 0;
    upgx = 0;
    upgy = 0;
    upgz = 0;
    upacc = 0;
    upgxyz = 0;
    sumupax = 0;
    sumupay = 0;
    sumupaz = 0;
    sumupgx = 0;
    sumupgy = 0;
    sumupgz = 0;
    for j = i : step - 1
        
        if ax(j + 1) > ax(j)
            upax = upax + 1;
            sumupax = sumupax + ax(j+1) - ax(j);
        end
        if ay(j + 1) > ay(j)
            upay = upay + 1;
            sumupay = sumupay + ay(j+1) - ay(j);
        end
        if az(j + 1) > az(j)
            upaz = upaz + 1;
            sumupaz = sumupaz + az(j+1) - az(j);
        end
        if gx(j + 1) > gx(j)
            upgx = upgx + 1;
            sumupgx = sumupgx + gx(j+1) - gx(j);
        end
        if gy(j + 1) > gy(j)
            upgy = upgy + 1;
            sumupgy = sumupgy + gy(j+1) - gy(j);
        end
        if gz(j + 1) > gz(j)
            upgz = upgz + 1;
            sumupgz = sumupgz + gz(j+1) - gz(j);
        end
        if acc(j + 1) > acc(j)
            upacc = upacc + 1;
        end
        if gxyz(j + 1) > gxyz(j)
            upgxyz = upgxyz + 1;
        end
        
        
        
    end
    
    meanabsax = mean(absax(i:i+step-1));
    meanabsay = mean(absay(i:i+step-1));
    meanabsaz = mean(absaz(i:i+step-1));
    meanabsgx = mean(absgx(i:i+step-1));
    meanabsgy = mean(absgy(i:i+step-1));
    meanabsgz = mean(absgz(i:i+step-1));

    divax = meanabsax / meanacc;
    divay = meanabsay / meanacc;
    divaz = meanabsaz / meanacc;
    divgx = meanabsgx / meangxyz;
    divgy = meanabsgy / meangxyz;
    divgz = meanabsgz / meangxyz;
    if printflag == 1
        meanabsax
        meanabsay
        meanabsaz
        meanabsgx
        meanabsgy
        meanabsgz
    end
        feature = [feature meanax meanay meanaz meangx meangy meangz meanacc meangxyz...
                varax varay varaz vargx vargy vargz varacc vargxyz...
                stdax stday stdaz stdgx stdgy stdgz stdacc stdgxyz...
                maxax maxay maxaz maxgx maxgy maxgz maxacc maxgxyz... % 25
                minax minay minaz mingx mingy mingz minacc mingxyz...
                sumslpax sumslpay sumslpaz sumslpgx sumslpgy sumslpgz sumslpacc sumslpgxyz... %41-46
                sumupax sumupay sumupaz sumupgx sumupgy sumupgz ...
                coraxay coraxaz coraxgx coraxgy coraxgz corayaz ...
                coraygx coraygy coraygz corazgx corazgy corazgz ...
                corgxgy corgxgz corgygz...
                upax upay upaz upgx upgy upgz upacc upgxyz...
                meanabsax meanabsay meanabsaz meanabsgx meanabsgy meanabsgz...
                divax divay divaz divgx divgy divgz...
                ];
    
end


end












