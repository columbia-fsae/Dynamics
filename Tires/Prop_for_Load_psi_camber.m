function A = Prop_for_Load_psi_camber(filename_mat, Prop1 , Prop2, FZ, range, psi, IA)

% Sorts matlab file into a matrix with only lateral force(FY) and slip 
% angle (SA) data points for a specified load
% For: http://www.fsaettc.org/ data
% Output: matrix (nx2) with column 1 = FY and column 2 = SA

F_Z = getfield(load(filename_mat, 'FZ'), 'FZ');
Prop_1 = getfield(load(filename_mat, Prop1), Prop1);
Prop_2= getfield(load(filename_mat, Prop2), Prop2);
P = getfield(load(filename_mat, 'P'), 'P');
I_A = getfield(load(filename_mat, 'IA'), 'IA');

matrix = horzcat(F_Z, Prop_2, Prop_1, P, I_A);
num_of_data_pts = size(matrix(:,1));

A = [];
for k = 1:num_of_data_pts;
    if all(matrix(k,1) <= FZ + range & matrix(k,1) >= FZ - range);
        if all(matrix(k,4) <= psi + .75 & matrix(k,4) >= FZ - .75);
            if all(matrix(k,5) <= IA + .5 & matrix(k,5) >= IA - .5);
                A = [A; matrix(k,2:3)];
            end
        end
    end
end


end