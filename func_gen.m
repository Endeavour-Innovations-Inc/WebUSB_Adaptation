t = (0:0.01:32);
t = t(:);

A = 0.5*(1.15 + sin(t));
A = A(:);

B = 0.5*(1.15 + square(0.5*t));
B = B(:);

C = 0.5*(1.15 + sawtooth(t,1/2));
C = C(:);

E = 0.5*(1.15 + sin(t) + randn(size(t))/30);
E = E(:);

header = ["t", "data"];

to_csv('sin_gen.csv', [t, A], header);
to_csv('square_gen.csv', [t, B], header);
to_csv('tri_gen.csv', [t, C], header);
to_csv('noisy_sin_gen.csv', [t, E], header);

t = 0:1/1e3:16;
t = t(:);
D = 0.5*(1.15 + (square(pi*t,37)+randn(size(t))/50));
D = D(:);

to_csv('sqr_wgn_gen.csv', [t, D], header);

function to_csv(filename, data, header)
    datatable = array2table(data);
    datatable.Properties.VariableNames(1:length(header)) = header;
    writetable(datatable, filename);
end
