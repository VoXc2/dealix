/**
 * DEALIX REACT COMPONENT LIBRARY
 * Premium AI Revenue Operations System
 * Production-ready components with full TypeScript support
 */

import React, { ReactNode, ButtonHTMLAttributes, InputHTMLAttributes } from 'react';

// ===== TYPE DEFINITIONS =====

type ButtonVariant = 'primary' | 'secondary' | 'accent' | 'ghost' | 'success' | 'error';
type ButtonSize = 'sm' | 'md' | 'lg' | 'xl';
type CardVariant = 'default' | 'elevated' | 'navy' | 'bordered';
type BadgeVariant = 'default' | 'primary' | 'success' | 'error' | 'warning' | 'info' | 'gold';
type InputVariant = 'default' | 'error' | 'success';
type ToastType = 'success' | 'error' | 'warning' | 'info';

// ===== BUTTON COMPONENT =====

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  block?: boolean;
  children: ReactNode;
  icon?: ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  block = false,
  icon,
  children,
  className = '',
  ...props
}) => {
  const baseClasses = 'btn';
  const variantClass = `btn-${variant}`;
  const sizeClass = `btn-${size}`;
  const blockClass = block ? 'btn-block' : '';

  return (
    <button
      className={`${baseClasses} ${variantClass} ${sizeClass} ${blockClass} ${className}`.trim()}
      {...props}
    >
      {icon && <span className="btn-icon">{icon}</span>}
      {children}
    </button>
  );
};

// ===== CARD COMPONENT =====

interface CardProps {
  variant?: CardVariant;
  children: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
  icon?: ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  variant = 'default',
  children,
  header,
  footer,
  icon,
  className = '',
}) => {
  const variantClass = variant !== 'default' ? `card--${variant}` : '';

  return (
    <div className={`card ${variantClass} ${className}`.trim()}>
      {(header || icon) && (
        <div className="card-header">
          {icon && <div className="card-icon">{icon}</div>}
          {header && <div>{header}</div>}
        </div>
      )}
      <div className="card-content">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
};

// ===== INPUT COMPONENT =====

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  variant?: InputVariant;
  icon?: ReactNode;
  iconPosition?: 'left' | 'right';
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  hint,
  variant = 'default',
  icon,
  iconPosition = 'right',
  className = '',
  ...props
}) => {
  const variantClass = variant !== 'default' ? `input--${variant}` : '';

  return (
    <div className="input-group">
      {label && <label htmlFor={props.id}>{label}</label>}
      <div style={{ position: 'relative' }}>
        <input
          className={`input ${variantClass} ${className}`.trim()}
          {...props}
        />
        {icon && (
          <div className={`input-icon input-icon--${iconPosition}`}>
            {icon}
          </div>
        )}
      </div>
      {error && <div className="input-error">{error}</div>}
      {hint && !error && <div className="input-hint">{hint}</div>}
    </div>
  );
};

// ===== TEXTAREA COMPONENT =====

interface TextAreaProps extends InputHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  hint?: string;
  rows?: number;
}

export const TextArea: React.FC<TextAreaProps> = ({
  label,
  error,
  hint,
  rows = 4,
  className = '',
  ...props
}) => {
  return (
    <div className="input-group">
      {label && <label>{label}</label>}
      <textarea
        className={`input ${className}`.trim()}
        rows={rows}
        {...(props as any)}
      />
      {error && <div className="input-error">{error}</div>}
      {hint && !error && <div className="input-hint">{hint}</div>}
    </div>
  );
};

// ===== BADGE COMPONENT =====

interface BadgeProps {
  variant?: BadgeVariant;
  children: ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  children,
  className = '',
}) => {
  const variantClass = variant !== 'default' ? `badge--${variant}` : '';

  return (
    <span className={`badge ${variantClass} ${className}`.trim()}>
      {children}
    </span>
  );
};

// ===== MODAL COMPONENT =====

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
  footer?: ReactNode;
  closeButton?: boolean;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
  closeButton = true,
}) => {
  if (!isOpen) return null;

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {(title || closeButton) && (
          <div className="modal-header">
            {title && <h2>{title}</h2>}
            {closeButton && (
              <button
                className="modal-close"
                onClick={onClose}
                aria-label="Close modal"
              >
                ✕
              </button>
            )}
          </div>
        )}
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-footer">{footer}</div>}
      </div>
    </div>
  );
};

// ===== TOAST COMPONENT =====

interface ToastProps {
  message: string;
  type?: ToastType;
  onClose?: () => void;
  duration?: number;
  icon?: ReactNode;
}

export const Toast: React.FC<ToastProps> = ({
  message,
  type = 'info',
  onClose,
  duration = 3000,
  icon,
}) => {
  React.useEffect(() => {
    if (duration && onClose) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  return (
    <div className={`toast toast--${type}`}>
      {icon && <div className="toast-icon">{icon}</div>}
      <div className="toast-message">{message}</div>
      {onClose && (
        <button className="toast-close" onClick={onClose}>
          ✕
        </button>
      )}
    </div>
  );
};

// ===== NAVBAR COMPONENT =====

interface NavbarProps {
  brand: string | ReactNode;
  logo?: string | ReactNode;
  items?: Array<{ label: string; href: string; active?: boolean }>;
  actions?: ReactNode;
  onMenuToggle?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  brand,
  logo,
  items = [],
  actions,
  onMenuToggle,
}) => {
  return (
    <nav className="navbar">
      <a href="/" className="navbar-brand">
        {logo && <span className="navbar-logo">{logo}</span>}
        {brand}
      </a>
      {items.length > 0 && (
        <ul className="navbar-menu">
          {items.map((item) => (
            <li key={item.href}>
              <a
                href={item.href}
                className={item.active ? 'active' : ''}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      )}
      {actions && <div className="navbar-actions">{actions}</div>}
      {onMenuToggle && (
        <button className="navbar-toggle" onClick={onMenuToggle}>
          ☰
        </button>
      )}
    </nav>
  );
};

// ===== CONTAINER COMPONENT =====

interface ContainerProps {
  children: ReactNode;
  className?: string;
}

export const Container: React.FC<ContainerProps> = ({
  children,
  className = '',
}) => {
  return <div className={`container ${className}`.trim()}>{children}</div>;
};

// ===== GRID COMPONENT =====

interface GridProps {
  children: ReactNode;
  columns?: number;
  gap?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Grid: React.FC<GridProps> = ({
  children,
  columns = 3,
  gap = 'md',
  className = '',
}) => {
  const gapClass = `grid--gap-${gap === 'sm' ? 4 : gap === 'lg' ? 8 : 6}`;
  const style = {
    gridTemplateColumns: `repeat(auto-fit, minmax(${300 / columns}px, 1fr))`,
  };

  return (
    <div className={`grid ${gapClass} ${className}`.trim()} style={style}>
      {children}
    </div>
  );
};

// ===== FLEX COMPONENT =====

interface FlexProps {
  children: ReactNode;
  direction?: 'row' | 'col';
  justify?: 'start' | 'center' | 'between' | 'end';
  items?: 'start' | 'center' | 'end' | 'stretch';
  gap?: number;
  className?: string;
}

export const Flex: React.FC<FlexProps> = ({
  children,
  direction = 'row',
  justify = 'start',
  items = 'stretch',
  gap = 16,
  className = '',
}) => {
  const style: React.CSSProperties = {
    display: 'flex',
    flexDirection: direction === 'col' ? 'column' : 'row',
    justifyContent:
      justify === 'between'
        ? 'space-between'
        : justify === 'center'
        ? 'center'
        : 'flex-start',
    alignItems:
      items === 'center'
        ? 'center'
        : items === 'end'
        ? 'flex-end'
        : 'flex-start',
    gap,
  };

  return (
    <div className={className} style={style}>
      {children}
    </div>
  );
};

// ===== HERO COMPONENT =====

interface HeroProps {
  title: string;
  subtitle?: string;
  cta?: ReactNode;
  image?: string;
  className?: string;
}

export const Hero: React.FC<HeroProps> = ({
  title,
  subtitle,
  cta,
  image,
  className = '',
}) => {
  return (
    <section
      className={`hero-demo ${className}`.trim()}
      style={
        image
          ? {
              backgroundImage: `url(${image})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }
          : {}
      }
    >
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
      {cta && <div style={{ marginTop: '24px' }}>{cta}</div>}
    </section>
  );
};

// ===== FORM COMPONENT =====

interface FormProps {
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  children: ReactNode;
  className?: string;
}

export const Form: React.FC<FormProps> = ({
  onSubmit,
  children,
  className = '',
}) => {
  return (
    <form className={className} onSubmit={onSubmit}>
      {children}
    </form>
  );
};

// ===== DIVIDER COMPONENT =====

interface DividerProps {
  className?: string;
}

export const Divider: React.FC<DividerProps> = ({ className = '' }) => {
  return <hr className={`divider ${className}`.trim()} />;
};

// ===== SKELETON LOADER COMPONENT =====

interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  rounded?: boolean;
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width = '100%',
  height = '20px',
  rounded = false,
  className = '',
}) => {
  return (
    <div
      className={`skeleton ${rounded ? 'skeleton--rounded' : ''} ${className}`.trim()}
      style={{
        width,
        height,
        background: 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)',
        backgroundSize: '200% 100%',
        animation: 'shimmer 2s infinite',
      }}
    />
  );
};

// ===== PAGINATION COMPONENT =====

interface PaginationProps {
  total: number;
  current: number;
  onChange: (page: number) => void;
  className?: string;
}

export const Pagination: React.FC<PaginationProps> = ({
  total,
  current,
  onChange,
  className = '',
}) => {
  const pages = Array.from({ length: total }, (_, i) => i + 1);

  return (
    <div className={`pagination ${className}`.trim()} style={{ display: 'flex', gap: '8px' }}>
      {pages.map((page) => (
        <button
          key={page}
          onClick={() => onChange(page)}
          className={`btn btn-${page === current ? 'primary' : 'secondary'} btn-sm`}
        >
          {page}
        </button>
      ))}
    </div>
  );
};

// ===== ACCORDION COMPONENT =====

interface AccordionItem {
  id: string;
  title: string;
  content: ReactNode;
}

interface AccordionProps {
  items: AccordionItem[];
  defaultOpen?: string;
  className?: string;
}

export const Accordion: React.FC<AccordionProps> = ({
  items,
  defaultOpen,
  className = '',
}) => {
  const [openId, setOpenId] = React.useState<string | undefined>(defaultOpen);

  return (
    <div className={`accordion ${className}`.trim()}>
      {items.map((item) => (
        <div key={item.id} className="accordion-item" style={{ marginBottom: '12px' }}>
          <button
            className="accordion-trigger"
            onClick={() => setOpenId(openId === item.id ? undefined : item.id)}
            style={{
              width: '100%',
              padding: '16px',
              background: openId === item.id ? '#F3F4F6' : 'white',
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              cursor: 'pointer',
              textAlign: 'left',
              fontWeight: '600',
            }}
          >
            {item.title}
            <span style={{ float: 'right' }}>
              {openId === item.id ? '−' : '+'}
            </span>
          </button>
          {openId === item.id && (
            <div
              className="accordion-content"
              style={{
                padding: '16px',
                background: '#F3F4F6',
                borderRadius: '0 0 8px 8px',
                marginTop: '-1px',
              }}
            >
              {item.content}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

// ===== BREADCRUMB COMPONENT =====

interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
}

export const Breadcrumb: React.FC<BreadcrumbProps> = ({
  items,
  className = '',
}) => {
  return (
    <nav className={`breadcrumb ${className}`.trim()} aria-label="Breadcrumb">
      <ol style={{ display: 'flex', gap: '8px', listStyle: 'none', padding: 0 }}>
        {items.map((item, index) => (
          <li key={index} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {item.href ? (
              <a href={item.href}>{item.label}</a>
            ) : (
              <span style={{ color: '#6B7280' }}>{item.label}</span>
            )}
            {index < items.length - 1 && <span>/</span>}
          </li>
        ))}
      </ol>
    </nav>
  );
};

export default {
  Button,
  Card,
  Input,
  TextArea,
  Badge,
  Modal,
  Toast,
  Navbar,
  Container,
  Grid,
  Flex,
  Hero,
  Form,
  Divider,
  Skeleton,
  Pagination,
  Accordion,
  Breadcrumb,
};
