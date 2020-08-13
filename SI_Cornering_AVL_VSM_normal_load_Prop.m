
% AVL VSM Tire fits
clear all

% 250
Tire_250 = Prop_for_Load_psi_camber('A1965raw1.mat', 'FX', 'SR', -1100, 4, 85, 0);
%Tire_250_fit = tire_data_fit(Tire_250, 'poly3');
%sortrows(Tire_250_fit);
xdata = Tire_250(:,1);
Fx = Tire_250(:,2);
plot(xdata, Fx)
NormalLoad = 250;
%save('Tire_250', 'Fy', 'NormalLoad', 'xdata');
hold on

% 200
Tire_200 = Prop_for_Load_psi_camber('A1965raw1.mat', 'FX', 'SR', -889, 4, 85, 0);
%Tire_200_fit = tire_data_fit(Tire_200, 'poly3');
xdata = Tire_200(:,1);
Fx = Tire_200(:,2);
plot(xdata, Fx)
NormalLoad = 200;
save('Tire_200', 'Fx', 'NormalLoad', 'xdata');

% 150
Tire_150 = - Prop_for_Load_psi_camber('A1965raw1.mat', 'FX', 'SR', -667, 2, 85, 2);
%Tire_150_fit = tire_data_fit(Tire_150, 'poly3');
xdata = Tire_150(:,1);
Fx = Tire_150(:,2);
plot(xdata, Fx)
NormalLoad = 150;
save('Tire_150', 'Fx', 'NormalLoad', 'xdata');

% 100
Tire_100 = Prop_for_Load_psi_camber('A1965raw1.mat', 'FX', 'SR', -444, 4, 85, 2);
%Tire_100_fit = tire_data_fit(Tire_100, 'poly3');
xdata = Tire_100(:,1);
Fx = Tire_100(:,2);
plot(xdata, Fx)
NormalLoad = 100;
save('Tire_100', 'Fx', 'NormalLoad', 'xdata');

% 50
Tire_50 = -Prop_for_Load_psi_camber('A1965raw1.mat', 'FX', 'SR', -222, 4, 85, 2);
%Tire_50_fit = tire_data_fit(Tire_50, 'poly3');
xdata = Tire_50(:,1);
Fx = Tire_50(:,2);
plot(xdata, Fx)
NormalLoad = 50;
save('Tire_50', 'Fx', 'NormalLoad', 'xdata');
ylabel('FX (lbs)')
xlabel('SR')
%legend('250','200', '150', '100', '50')
hold off